import React, { useEffect, useState } from "react";
import "../styles/NewDestination.css";

interface Country {
  id: number;
  country: string;
}
interface City {
  id: number;
  city: string;
}

const NewDestination = () => {
  const countriesGETUrl = "http://localhost:5175/api/country/";
  const citiesGETUrl = "http://localhost:5175/api/city/";
  const [listCountries, setListCountries] = useState<Country[]>([]);
  const [lisCities, setListCities] = useState<City[]>([]);
  const [selectedCountryId, setSelectedCountryId] = useState<number | null>(
    null
  );
  const [selectedCityId, setSelectedCityId] = useState<number | null>(null);
  const [newCountryInput, setNewCountryInput] = useState<string>("");
  const [cityInput, setCityInput] = useState<string>("");
  const [depatureCity, setDepatureCity] = useState<string>("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [price, setPrice] = useState<number | "">(0);
  const [slot, setSlot] = useState<number | "">(0);
  const [imgUrls, setImgUrls] = useState<string[]>(["", ""]);
  const [plans, setPlans] = useState<string[]>([]);

  const fetchAllCountries = async () => {
    try {
      const response = await fetch(countriesGETUrl);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const countries = await response.json();
      setListCountries(countries);
    } catch (error) {
      console.log("Got an error: ", error);
    }
  };
  const fetchAllCities = async () => {
    try {
      const response = await fetch(citiesGETUrl);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const cities = await response.json();
      setListCities(cities);
    } catch (error) {
      console.log("Got an error: ", error);
    }
  };

  useEffect(() => {
    fetchAllCountries();
    fetchAllCities();
  }, []);

  const handleSetSelectedCountry = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const selectedId = event.target.value
      ? parseInt(event.target.value, 10)
      : null;
    setSelectedCountryId(selectedId);
    // setNewCountryInput("");
  };

  const handleSetSelectedCity = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const selectedId = event.target.value
      ? parseInt(event.target.value, 10)
      : null;
    setSelectedCityId(selectedId);
    // setNewCountryInput("");
  };

  const handleNewCountryInputChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setNewCountryInput(event.target.value);
  };

  const handleCityInputChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setCityInput(event.target.value);
  };

  const handleSubmitCity = (event: React.FormEvent) => {
    event.preventDefault();

    if (selectedCountryId && cityInput.trim() !== "") {
      console.log({
        id: selectedCountryId,
        city: cityInput.trim(),
      });
      fetch("http://localhost:5175/api/city", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
        },
        body: JSON.stringify({
          CountryDestinationId: selectedCountryId,
          city: cityInput,
          listImgUrl: imgUrls,
        }),
      }).then((responseFromServer) => {
        if (responseFromServer.ok) {
          alert("Add new city successfully, Reload to add new Tour");
          setCityInput("");
          setImgUrls(["", ""]);
        } else {
          alert("Something wrong, try again");
        }
      });
    } else {
      console.log("Please select a country and enter a city.");
    }
  };

  const handleSubmitCountry = (event: React.FormEvent) => {
    event.preventDefault();
    if (newCountryInput.trim() === "") {
    } else {
      fetch("http://localhost:5175/api/country", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
        },
        body: JSON.stringify({
          country: newCountryInput,
        }),
      }).then((responseFromServer) => {
        if (responseFromServer.ok) {
          alert("Add new country successfully, Reload to add new City");
        } else {
          alert("Something wrong, try again");
        }
      });
    }
  };
  const handleInputChange = (index: number, value: string) => {
    const updatedInputs = [...imgUrls];
    updatedInputs[index] = value;
    setImgUrls(updatedInputs);
  };

  const handleAddDay = () => {
    setPlans((prevPlans) => [...prevPlans, ""]); // thêm một ô input mới vào danh sách
  };

  const handleChange = (index: number, value: string) => {
    const updatedPlans = [...plans];
    updatedPlans[index] = value; // cập nhật giá trị cho ô input ở vị trí index
    setPlans(updatedPlans);
  };
  const handleRemoveDay = (index: number) => {
    const updatedPlans = plans.filter((_, i) => i !== index); // loại bỏ ô input ở vị trí index
    setPlans(updatedPlans);
  };
  return (
    <div>
      <div id="destination_header">
        <h3>Add new Destination</h3>
      </div>
      <div id="destination_container">
        <div id="country_container">
          <h4>Add new Country</h4>
          <form onSubmit={handleSubmitCountry}>
            <input
              type="text"
              className="inputField"
              value={newCountryInput}
              onChange={handleNewCountryInputChange}
              placeholder="New Country..."
            />
            <button id="submit_btn" type="submit">
              Send
            </button>
          </form>
        </div>

        <div id="city_container">
          <h4>Add new City</h4>
          <div className="dropdown-container">
            <label htmlFor="dropdown">Country</label>
            <select
              id="dropdown"
              value={selectedCountryId ?? ""}
              onChange={handleSetSelectedCountry}
            >
              <option value="" disabled>
                Select an option
              </option>
              {listCountries.map((option: Country) => (
                <option key={option.id} value={option.id}>
                  {option.country}
                </option>
              ))}
            </select>
          </div>

          <form id="city_form" onSubmit={handleSubmitCity}>
            <input
              type="text"
              className="inputField"
              value={cityInput}
              onChange={handleCityInputChange}
              placeholder="City..."
              required
            />
            <input
              type="text"
              className="inputField"
              value={imgUrls[0]}
              onChange={(e) => handleInputChange(0, e.target.value)}
              placeholder="Image Url.."
              required
            />
            <input
              type="text"
              className="inputField"
              value={imgUrls[1]}
              onChange={(e) => handleInputChange(1, e.target.value)}
              placeholder="Image Url.."
              required
            />
            <button id="submit_btn" type="submit">
              Send
            </button>
          </form>
        </div>
      </div>
      <div id="addtour_container">
        <h4>Add new Tour</h4>
        <div className="dropdown-container">
          <label htmlFor="dropdown">City</label>
          <select
            id="dropdown"
            value={selectedCountryId ?? ""}
            onChange={handleSetSelectedCity}
          >
            <option value="" disabled>
              Select an option
            </option>
            {lisCities.map((option: City) => (
              <option key={option.id} value={option.id}>
                {option.city}
              </option>
            ))}
          </select>
        </div>

        <form
          id="tour_form"
          onSubmit={(event) => {
            event.preventDefault();
            fetch("http://localhost:5175/api/tour", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${sessionStorage.getItem("jwt")}`,
              },
              body: JSON.stringify({
                country: newCountryInput,
                CityDestinationId: selectedCityId,
                DepartureLocation: depatureCity,
                StartDate: startDate,
                EndDate: endDate,
                Price: price,
                AvailableSlots: slot,
                plans: plans,
              }),
            }).then((responseFromServer) => {
              if (responseFromServer.ok) {
                alert("Add new Tour successfully");
                setDepatureCity("");
                setStartDate("");
                setEndDate("");
                setPrice("");
                setSlot("");
                setPlans([]);
              } else {
                alert("Something wrong, try again");
              }
            });
          }}
        >
          <label htmlFor="tour_plan">Deparature Location</label>
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
            required
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
            required
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
                value={plan}
                onChange={(event) => handleChange(index, event.target.value)}
                placeholder={`Add plan for day ${index + 1}`}
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
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default NewDestination;
