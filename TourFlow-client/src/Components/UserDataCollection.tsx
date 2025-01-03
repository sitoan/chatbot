import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import NavigationBar from "./NavigationBar";
import Footer from "./Footer";
import "../styles/UserDataCollection.css";
type TableData = {
  phoneNumber: string;
  starPos: string;
  endPos: string;
  startDate: string;
  duration: string;
  budget: number | null;
  availableSlot: number;
};

const UserDataCollection = () => {
  const { userid } = useParams();
  const [data, setData] = useState<TableData[]>([]);
  const fetchUserData = async (userId: string) => {
    var response = await fetch(
      `http://localhost:5175/api/userdatacollection/${userId}`
    );
    if (response.ok) {
      setData(await response.json());
    } else {
      console.log("failde to fetch in fetchUserData (UserDataCollection)");
    }
  };
  useEffect(() => {
    console.log(userid);
    fetchUserData(userid || "");
  }, []);
  useEffect(() => {
    console.log(data);
  }, [data]);

  return (
    <div>
      <NavigationBar />
      <div id="userDataCollection_container">
        <h3>Additional User's information from AI Service</h3>
        <div className="table-container">
          <table className="user-table">
            <thead>
              <tr>
                <th>Phone Number</th>
                <th>Departure from</th>
                <th>Expected Destination</th>
                <th>Expected Date</th>
                <th>Duration</th>
                <th>Budget</th>
                <th>Participants</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  <td>{item.phoneNumber}</td>
                  <td>{item.starPos}</td>
                  <td>{item.endPos}</td>
                  <td>{item.startDate}</td>
                  <td>{item.duration}</td>
                  <td>{item.budget}</td>
                  <td>{item.availableSlot}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default UserDataCollection;
