import { createContext } from "react";

interface City {
  id: number;
  city: string;
}

interface searchType {
  destination: string;
  setDestination: (newValue: string) => void;
  currentCity: City;
  setCurrentCity: (newValue: City) => void;
  citiesUrl: string;
  setCitiesUrl: (newValue: string) => void;
  currentPage: number;
  setCurrentPage: (newValue: number) => void;
  totalPages: number;
  setTotalPages: (newValue: number) => void;
  login: boolean;
  setLogin: (newValue: boolean) => void;
}

export const TourFlowContext = createContext<searchType | undefined>(undefined);
