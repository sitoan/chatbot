import { useEffect, useState } from "react";
import "../styles/UpdateTourModal.css";
import { Tour } from "../index";
import { Alert } from "react-bootstrap";
interface UpdateTourModalProps {
  tourId: number;
  onClose: () => void;
  onDeleteTour: () => void;
}
interface UpdateTourPlan {
  id: number;
  detailPlan: string;
}
const UpdateTourModal: React.FC<UpdateTourModalProps> = ({
  tourId,
  onClose,
  onDeleteTour,
}) => {
  const [tour, setTour] = useState<Tour>();
  useEffect(() => {
    const fetchTourInfor = async (tourId: any) => {
      const url = `http://localhost:5175/api/tour/${tourId}`;

      try {
        const response = await fetch(url);
        const result = await response.json();
        console.log(tour);
        setTour(result);
      } catch (error) {
        console.log("Got error in TourDetail: ", error);
      }
    };
    const fetchTourPlan = async (tourId: any) => {
      const url = `http://localhost:5175/api/tourplan/withId/${tourId}`;

      try {
        const response = await fetch(url);
        const result = await response.json();
        setPlans(result);
      } catch (error) {
        console.log("Got error in Tourplan: ", error);
      }
    };
    fetchTourInfor(tourId);
    fetchTourPlan(tourId);
  }, []);
  const [depatureCity, setDepatureCity] = useState<string | undefined>();
  const [startDate, setStartDate] = useState<string | undefined>();
  const [endDate, setEndDate] = useState<string | undefined>();
  const [price, setPrice] = useState<number | "" | undefined>();
  const [slot, setSlot] = useState<number | "" | undefined>();
  const [plans, setPlans] = useState<UpdateTourPlan[]>([]);
  const [newPlans, setNewPlans] = useState<string[]>([]);

  useEffect(() => {
    setDepatureCity(tour?.departureLocation);
    setStartDate(tour?.startDate);
    setEndDate(tour?.endDate);
    setPrice(tour?.price);
    setSlot(tour?.availableSlots);
  }, [tour]);
  const handleChange = (id: number, updatedPlan: UpdateTourPlan) => {
    setPlans((prevPlans) =>
      prevPlans.map((plan) =>
        plan.id === id ? { ...plan, ...updatedPlan } : plan
      )
    );
  };
  const handleChange2 = (index: number, value: string) => {
    const updatedPlans = [...newPlans];
    updatedPlans[index] = value; // cập nhật giá trị cho ô input ở vị trí index
    setNewPlans(updatedPlans);
  };
  const handleRemoveDay = (index: number) => {
    const updatedPlans = plans.filter((_, i) => i !== index); // loại bỏ ô input ở vị trí index
    setPlans(updatedPlans);
  };

  const handleAddDay = () => {
    setNewPlans((prevPlans) => [...prevPlans, ""]); // thêm một ô input mới vào danh sách
  };
  const deleteTour = async (tourId: number): Promise<void> => {
    try {
      const response = await fetch(`http://localhost:5175/api/tour/${tourId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
        },
      });

      if (response.ok) {
        onDeleteTour();
        alert("Tour deleted successfully");
      } else {
        console.error("Failed to delete the tour");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div id="update_tour_modal" className="modal-overlay">
      <div className="modal-content">
        <h2>Update Tour</h2>
        <form
          id="tour_form"
          onSubmit={(event) => {
            event.preventDefault();

            console.log("depatureCity: ", depatureCity);
            console.log("startDate: ", startDate);
            console.log("endDate: ", endDate);
            console.log("price: ", price);
            console.log("slot: ", slot);
            console.log("plans: ", plans);

            console.log("newPlans: ", newPlans);
            fetch(`http://localhost:5175/api/tour/${tourId}`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
              },
              body: JSON.stringify({
                DepartureLocation: depatureCity,
                StartDate: startDate,
                EndDate: endDate,
                Price: price,
                AvailableSlots: slot,
                plans: plans,
                newPlans: newPlans,
              }),
            }).then((responseFromServer) => {
              if (responseFromServer.ok) {
                alert("Successfully");
                onClose();
              } else {
                alert("Something wrong, try again");
              }
            });
          }}
        >
          <input
            type="text"
            className="inputField"
            value={depatureCity}
            onChange={(event) => {
              setDepatureCity(event.target.value);
            }}
            placeholder="Go from..."
            required
          />
          <label htmlFor="start-date">Start Date:</label>
          <input
            type="date"
            id="start-date"
            name="startDate"
            value={startDate}
            onChange={(event) => {
              setStartDate(event.target.value);
            }}
          />

          <label htmlFor="end-date">End Date:</label>
          <input
            type="date"
            id="end-date"
            name="endDate"
            value={endDate}
            onChange={(event) => {
              setEndDate(event.target.value);
            }}
          />
          <label htmlFor="tour_plan">Tour Price </label>

          <input
            type="number"
            id="price"
            step="0.01"
            placeholder="Price"
            value={price}
            onChange={(event) => {
              const value = event.target.value;
              setPrice(value === "" ? "" : parseFloat(value));
            }}
            required
          />
          <label htmlFor="tour_plan">Available slots </label>

          <input
            type="number"
            id="slots"
            step="1"
            placeholder="Slots"
            value={slot}
            onChange={(event) => {
              const value = event.target.value;
              setSlot(value === "" ? "" : parseInt(value));
            }}
            required
          />
          <label htmlFor="tour_plan">Tour Plan</label>
          {plans.map((plan, index) => (
            <div key={index} style={{ marginBottom: "10px" }}>
              <input
                type="text"
                className="inputField"
                value={plan.detailPlan}
                onChange={(event) =>
                  handleChange(plan.id, {
                    id: plan.id,
                    detailPlan: event.target.value,
                  })
                }
                placeholder={plan.detailPlan}
                required
              />
              <button
                className="remove-btn"
                onClick={() => handleRemoveDay(index)}
              >
                Remove
              </button>
            </div>
          ))}
          {newPlans.map((plan, index) => (
            <div key={index} style={{ marginBottom: "10px" }}>
              <input
                type="text"
                className="inputField"
                value={plan}
                onChange={(event) => handleChange2(index, event.target.value)}
                required
              />
              <button
                className="remove-btn"
                onClick={() => handleRemoveDay(index)}
              >
                Remove
              </button>
            </div>
          ))}
          <button id="add_day" onClick={handleAddDay}>
            add day
          </button>

          <button id="submit_btn" type="submit">
            Update
          </button>
          <button
            onClick={() => deleteTour(tourId)}
            id="submit_btn"
            className="deleteBtn"
          >
            Delete this tour
          </button>
        </form>
        <button onClick={onClose} className="close-modal-btn">
          Close
        </button>
      </div>
    </div>
  );
};

export default UpdateTourModal;
