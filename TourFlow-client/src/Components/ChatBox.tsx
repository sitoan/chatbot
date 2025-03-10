import { useEffect, useRef, useState } from "react";
import "../styles/ChatBox.css";
import React from "react";
import { Link } from "react-router-dom";

interface MessageSender {
  sender: string;
  text: string;
}

interface MessageRecipient {
  recipient_id: string;
  text: string;
}
type Message = MessageSender | MessageRecipient;

const ChatBox = () => {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [val, setVal] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [messageList, setMessageList] = useState<Message[]>([]);
  const buttons = [
    {
      title: "Tìm tour",
      payload: "/request_tour_form",
    },
    {
      title: "Xem tour phổ biến",
      payload: "/show_tours",
    },
    {
      title: "Bạn muốn đặt tour ?",
      payload: "/request_customer_form",
    },
    {
      title: "Xoá lịch sử trò chuyện",
      payload: "/clean_slots",
    },
  ];

  const handleClick = (index: number) => {
    if (index === buttons.length - 1) {
      setMessageList([]); // Xóa danh sách tin nhắn
      console.log("Message list cleared!");
    }
  };

  const postMessageToAIService = async (
    sender: string | null,
    message: any
  ) => {
    try {
      // const res = await fetch("http://localhost:5111/api/home", {
      //test api
      const res = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sender, message }),
        mode: "cors",
      });
      if (!res.ok) {
        console.log("POST FAILED");
        throw new Error("Network response was not ok");
      }

      const data: MessageRecipient[] = await res.json();
      data.map((message) =>
        setMessageList((prevList) => [message, ...prevList])
      );
      console.log(messageList);
      // setMessageList((prevList) => [data, ...prevList]);
    } catch (error) {
      console.error(
        "Exception in postMessageToAIService in ChatBot.tsx",
        error
      );
    }
  };
  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setVal(e.target.value);
  }
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      console.log("Enter pressed"); // kiểm tra xem hàm có được gọi hai lần không

      scrollToBottom();
      setMessage(val);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const cleanArray = (arr: any) => {
    return arr.map((str: string) => str.replace(/\s+/g, " ").trim());
  };

  const processRecieveMessage = (message: string) => {
    if (Number(message) && Number(message) < 1000) {
      return Number(message);
    } else {
      const sentences = message.split("*");
      return cleanArray(sentences).join("<br>");
    }
  };
  const addMessageBox = (message: string, index: any, className: string) => {
    const processedMessage: any = processRecieveMessage(message);
    {
      if (typeof processedMessage != "number") {
        return (
          <div
            dangerouslySetInnerHTML={{ __html: processedMessage }}
            key={index}
            className={`message_box ${className}`}
          />
        );
      } else {
        return (
          <Link to={`/tourdetail?id=${processedMessage}`} key={index}>
            <div
              key={index}
              className={`message_box  ${className}  clickable_message`}
              onClick={() => {
                console.log("Tour ", processedMessage);
              }}
            >
              {"Explore more about tour: " + processedMessage.toString()}
            </div>
          </Link>
        );
      }
    }
  };
  useEffect(() => {
    scrollToBottom();
    if (message) {
      const newUserMessage: MessageSender = {
        sender: sessionStorage.getItem("id") ?? "",
        text: val,
      };
      setMessageList((prevList) => [newUserMessage, ...prevList]);
      postMessageToAIService(sessionStorage.getItem("id"), message);
    }
    setVal("");
  }, [message]);
  function isRecipientMessage(message: Message): message is MessageRecipient {
    return (message as MessageRecipient).recipient_id !== undefined;
  }
  return (
    <div id="container">
      <div id="chat_name">TourFlow ChatBot</div>
      <div id="messages_container">
        {messageList.map((message: Message, index) => {
          if (isRecipientMessage(message)) {
            return addMessageBox(message.text, index, "bot");
          } else {
            return addMessageBox(message.text, index, "user");
          }
        })}
      </div>
      <div id="button_container">
        {buttons.map((button, index) => (
          <div
            className="button"
            key={index}
            onClick={() => {
              handleClick(index);
              postMessageToAIService(
                sessionStorage.getItem("id"),
                button.payload
              );
              console.log(button.payload);
            }}
          >
            {button.title}
          </div>
        ))}
      </div>
      <input
        type="text"
        id="chat_input"
        placeholder="input yout message"
        value={val}
        onChange={handleChange}
        onKeyDown={(e: any) => {
          handleKeyPress(e);
        }}
      />
    </div>
  );
};

export default ChatBox;