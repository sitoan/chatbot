import { useEffect, useRef, useState } from "react";
import "../styles/Destination.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight, faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { useStringContext } from "../ContextAPI/TourFlowProvider";
interface City {
  id: number;
  city: string;
}
const Destination = () => {
  const [destinations, setDestinations] = useState<any[]>([]);
  const { citiesUrl, currentCity, setCurrentCity, destination } =
    useStringContext();

  const fetchData = async (allCitiesUrl: string) => {
    try {
      const response = await fetch(allCitiesUrl);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      // console.log(result);
      setDestinations(result);
    } catch (error) {
      console.log("Got an error: ", error);
    }
  };
  const allCitiesUrl = "http://localhost:5175/api/destination/cities";
  useEffect(() => {
    fetchData(allCitiesUrl);
  }, []);
  const filteredCities = destinations.filter((city) =>
    city.city.toLowerCase().includes(destination.toLowerCase())
  );

  function print(city: City) {
    setCurrentCity(city);
    console.log(city.city);
  }
  useEffect(() => {
    // console.log("from tourheader: ", citiesUrl);
    if (citiesUrl) {
      fetchData(citiesUrl);
    }
  }, [citiesUrl]);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    let scrollAmount = 0;
    const scrollStep = 1;
    const scrollInterval = 30;

    const autoScroll = () => {
      if (container) {
        if (scrollAmount >= container.scrollWidth - container.clientWidth) {
          scrollAmount = 0;
        } else {
          scrollAmount += scrollStep;
        }
        container.scrollLeft = scrollAmount;
      }
    };

    const intervalId = setInterval(autoScroll, scrollInterval);
    return () => clearInterval(intervalId);
  }, []);
  const backToAllCities = () => {
    setCurrentCity({
      id: -1,
      city: "All City",
    });
  };
  return (
    <div>
      <div id="tourheader-destinations" ref={containerRef}>
        {(filteredCities.length > 0 ? filteredCities : destinations).map(
          (city) => (
            <div
              className="destination-card"
              key={city.id}
              onClick={() => print(city)}
            >
              <span>{city.city}</span>
            </div>
          )
        )}
      </div>
      <div id="destination-header">
        <div className="tourheader-item1">
          <h3>{currentCity.city}</h3>
        </div>
        <div className="destination-item2" onClick={() => backToAllCities()}>
          <h3>Show all tours</h3>
        </div>
      </div>
    </div>
  );
};

export default Destination;
