import NavigationBar from "./NavigationBar";
import "../styles/CustomerProfile.css";
import { Link } from "react-router-dom";
import { useStringContext } from "../ContextAPI/TourFlowProvider";
import { useEffect, useState } from "react";

interface Order {
  departure: string;
  tourName: string;
  bookDate: string;
  slots: number;
  price: number;
  Paid: boolean;
}

const CustomerProfile = () => {
  const { setLogin } = useStringContext();
  const [order, setOrder] = useState<Order[]>([]);
  const handleLogout = () => {
    setLogin(false);
    sessionStorage.clear();
  };
  const fetchData = async (id: string) => {
    const response = await fetch(`http://localhost:5175/api/tourorder/${id}`);
    if (response.ok) {
      setOrder(await response.json());
    } else {
      console.log("Fail to fetch Order");
    }
  };

  useEffect(() => {
    fetchData(sessionStorage.getItem("id") ?? "");
  }, []);
  useEffect(() => {
    console.log(order);
  }, [order]);
  return (
    <div>
      <NavigationBar />
      <h3
        style={{
          marginLeft: "50%",
          transform: "translateX(-10%)",
          marginTop: "50px",
        }}
      >
        Your bookings
      </h3>

      <div className="table-container">
        <table className="tour-table">
          <thead>
            <tr>
              <th>Departure</th>
              <th>Tour Name</th>
              <th>Book Date</th>
              <th>Slots</th>
              <th>Price</th>
              <th>Paid</th>
            </tr>
          </thead>
          <tbody>
            {order.map((tour, index) => (
              <tr key={index}>
                <td>{tour.departure}</td>
                <td>{tour.tourName}</td>
                <td>
                  {tour.bookDate
                    ? new Date(tour.bookDate).toLocaleString()
                    : "N/A"}
                </td>
                <td>{tour.slots}</td>
                <td>{tour.price.toLocaleString()}</td>
                <td>{tour.Paid ? "Already" : "Pending"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Link to="/" id="redirect_logout">
        <div
          id="log_out"
          onClick={() => {
            handleLogout();
          }}
        >
          Log out
        </div>
      </Link>
    </div>
  );
};

export default CustomerProfile;
