// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { faArrowRight, faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { useEffect, useState } from "react";
import "../styles/TourHeader.css";
import { useStringContext } from "../ContextAPI/TourFlowProvider";
interface City {
  id: number;
  city: string;
}

const TourHeader = () => {
  const [cities, setCities] = useState<string[]>([]);
  const { destination, setDestination, setCitiesUrl } = useStringContext();
  const allCitiesUrl = "http://localhost:5175/api/destination/cities";
  const fetchData = async () => {
    try {
      const response = await fetch(allCitiesUrl);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const result = await response.json();
      const cityNames = result.map((item: City) => item.city.toLowerCase());
      setCities(cityNames);
    } catch (error) {
      console.log("Got an error: ", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);
  // useEffect(() => {
  //   console.log("hello: ", cities);
  // }, [cities]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      const inputValue = (event.target as HTMLInputElement).value.toLowerCase();
      if (inputValue === "" || inputValue == "all") {
        setCitiesUrl(allCitiesUrl);
      } else if (cities.includes(inputValue)) {
        setCitiesUrl(
          `http://localhost:5175/api/destination/city/${inputValue}`
        );
      } else {
        setCitiesUrl(
          `http://localhost:5175/api/destination/${destination}/cities`
        );
      }
      // console.log("Enter key pressed:", inputValue);
    }
  };
  return (
    <div id="tourheader-container">
      <div className="tourheader-item1">
        <h3>Popular Destinations</h3>
        <p>Unleash your Wanderlust</p>
      </div>
      <div className="tourheader-item2">
        <div id="search-area">
          <input
            id="search-bar"
            type="text"
            placeholder="Search..."
            onChange={(event) => {
              setDestination(event.target.value);
            }}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>
    </div>
  );
};

export default TourHeader;
