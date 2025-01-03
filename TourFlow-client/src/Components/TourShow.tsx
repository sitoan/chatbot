import React, { useState, useEffect } from "react";
import { useStringContext } from "../ContextAPI/TourFlowProvider";
import { Link } from "react-router-dom";
import { Tour } from "../index";
// import "../styles/TourShow.css";
import styles from "../styles/TourShow.module.css";
interface responseTourShow {
  data: Tour[];
  currentPage: number;
  totalPages: number;
}
const TourComponent: React.FC = () => {
  const [tours, setTours] = useState<Tour[]>([]);
  const { currentCity, setTotalPages, currentPage } = useStringContext();
  const fetchData = async (allTourUrl: string) => {
    try {
      const response = await fetch(allTourUrl);
      console.log("tourshow fetch executed");
      if (!response.ok) {
        throw new Error("Response was not ok");
      }
      var res: responseTourShow = await response.json();
      setTours(res.data);
      setTotalPages(res.totalPages);
    } catch (error) {
      console.log("Exception error: ", error);
    }
  };
  useEffect(() => {
    if (currentCity.id != -1) {
      const destinationToursUrl = `http://localhost:5175/api/tour/destination/${currentCity.id}`;
      fetchData(destinationToursUrl);
    } else {
      fetchData(`http://localhost:5175/api/tour?page=${currentPage}&limit=10`);
    }
  }, [currentCity, currentPage]);

  return (
    <div id={styles.tour_container}>
      {tours.map((tour) => (
        <Link to={`/tourdetail?id=${tour.id}`} key={tour.id}>
          <div
            key={tour.id}
            className={styles.tour_card}
            onClick={() => {
              console.log(`tour: ${tour.id}`);
            }}
          >
            <img
              src={
                tour.firstImageUrl ||
                "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8fA%3D%3D"
              }
              alt=""
              className={styles.background_img}
            />
            <div className={styles.content}>
              <h3>
                {tour.city}, {tour.country}
              </h3>
              <p>Departure: {tour.departureLocation}</p>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default TourComponent;
