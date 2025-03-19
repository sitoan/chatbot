import React, { useState, ReactNode, useContext } from "react";
import { TourFlowContext } from "./TourFlowContext";

interface TourFlowProp {
  children: ReactNode;
}
interface City {
  id: number;
  city: string;
}
export const TourFlowProvider: React.FC<TourFlowProp> = ({ children }) => {
  const [destination, setDestination] = useState<string>("");
  const [currentCity, setCurrentCity] = useState<City>({
    id: -1,
    city: "All City",
  });
  const [citiesUrl, setCitiesUrl] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [login, setLogin] = useState<boolean>(false);
  return (
    <TourFlowContext.Provider
      value={{
        destination,
        setDestination,
        currentCity,
        setCurrentCity,
        citiesUrl,
        setCitiesUrl,
        currentPage,
        setCurrentPage,
        totalPages,
        setTotalPages,
        login,
        setLogin,
      }}
    >
      {children}
    </TourFlowContext.Provider>
  );
};
export const useStringContext = () => {
  const context = useContext(TourFlowContext);
  if (!context) {
    throw new Error("useStringContext must be used within a StringProvider");
  }
  return context;
};
