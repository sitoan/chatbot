import { useEffect, useState } from "react";
import "../styles/ManageUser.css";
import { useNavigate } from "react-router-dom";

interface Tour {
  CityDestination: string;
  BookDate: string;
}

interface User {
  userId: number;
  name: string;
  email: string;
  avatar: string;
  tours: Tour[]; // Adjust this if tourBooked has other structures
}

const ManageUser = () => {
  const navigate = useNavigate();

  const fetchUsers = async (url: string) => {
    try {
      const response = await fetch(url);
      if (response.ok) {
        setUsers(await response.json());
      }
    } catch (Exception) {
      console.log("Error occuired in ", Exception);
    }
  };
  useEffect(() => {
    fetchUsers("http://localhost:5175/api/auth/");
  }, []);

  const [users, setUsers] = useState<User[]>([]);
  useEffect(() => {
    console.log(users);
  }, [users]);
  return (
    <div>
      <table className="user-info-table">
        <thead>
          <tr>
            <th>Avatar</th>
            <th>Name</th>
            <th>Email</th>
            <th>Tours</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user: any) => {
            return (
              <tr
                onClick={() => {
                  console.log("hiho");
                  navigate(`/userdatacollection/${user.userId}`);
                }}
                key={user.userId}
              >
                <td>
                  <img src={user.avatar} alt="Avatar" className="avatar" />
                </td>
                <td>{user.userName}</td>
                <td>{user.userEmail} </td>
                <td>
                  <div className="tours">
                    {user.tours.map((tour: any, tourIndex: any) => (
                      <div key={tourIndex} className="tour">
                        <strong>City:</strong> {tour.cityDestination} <br />
                        <strong>Book Date:</strong>{" "}
                        {tour.bookDate
                          ? new Date(tour.bookDate).toLocaleString()
                          : "Not booked"}
                      </div>
                    ))}
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default ManageUser;
