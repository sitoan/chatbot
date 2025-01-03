import { useEffect, useState } from "react";
import NavigationBar from "./NavigationBar";
import Banner from "./Banner";
import Contact from "./Contact";
import TourHeader from "./TourHeader";
import Destination from "./Destination";
import ChatBox from "./ChatBox";
import TourComponent from "./TourShow";
import PagesTourShow from "./PagesTourShow";
import { useStringContext } from "../ContextAPI/TourFlowProvider";

import Footer from "./Footer";

const MainPage = () => {
  const [botActivate, setBotActivate] = useState(false);
  const { login } = useStringContext();
  useEffect(() => {
    console.log("hihi");
  }, [login]);
  return (
    <div id="html">
      <NavigationBar />
      <Banner />
      <Contact />
      <TourHeader />
      <Destination />
      <TourComponent />
      <PagesTourShow />
      <div id="bot_activation" onClick={() => setBotActivate(!botActivate)}>
        TourFlow Bot
      </div>
      {botActivate && sessionStorage.getItem("jwt") && (
        <div id="bot_container">
          <ChatBox />
        </div>
      )}
      <Footer />
    </div>
  );
};

export default MainPage;
