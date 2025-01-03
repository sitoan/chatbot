import PagesTourShow from "./PagesTourShow";
import UpdateTourModal from "./UpdateTourModal";
import "../styles/ToursManagement.css";
import { useStringContext } from "../ContextAPI/TourFlowProvider";
import { Tour } from "../index";
import { useEffect, useState } from "react";
import styles from "../styles/TourShow.module.css";
interface responseTourShow {
  data: Tour[];
  currentPage: number;
  totalPages: number;
}
const ToursManagement = () => {
  const [tours, setTours] = useState<Tour[]>([]);
  const { currentCity, setTotalPages, currentPage } = useStringContext();
  const [isOpenModal, setIsOpenModal] = useState(false);
  const [chosenCity, setChosenCity] = useState(-1);
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
  useEffect(() => {
    console.log("chosen cicty: ", chosenCity);
    console.log("modal open: ", isOpenModal);
  }, [chosenCity, isOpenModal]);
  const handleCloseModal = () => {
    setIsOpenModal(false);
    setChosenCity(-1);
  };
  const handleDeleteTour = () => {
    fetchData(`http://localhost:5175/api/tour?page=${currentPage}&limit=10`);
  };

  return (
    <div id="tours_management_container">
      <div id={styles.tour_container}>
        {tours.map((tour) => (
          <div
            key={tour.id}
            className={styles.tour_card}
            onClick={() => {
              console.log(`tour: ${tour.id}`);
              setIsOpenModal(true);
              setChosenCity(tour.id);
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
        ))}
      </div>
      <PagesTourShow />

      {isOpenModal && (
        <UpdateTourModal
          tourId={chosenCity}
          onClose={handleCloseModal}
          onDeleteTour={handleDeleteTour}
        />
      )}
    </div>
  );
};

export default ToursManagement;
