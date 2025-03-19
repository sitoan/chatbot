export interface Tour {
  id: number;
  departureLocation: string;
  city: string;
  country: string;
  startDate: string;
  endDate: string;
  duration: string;
  price: number;
  availableSlots: number;
  tourPlans: string[];
  firstImageUrl: string;
}
