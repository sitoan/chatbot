import "./ContextAPI/TourFlowProvider";
import MainPage from "./Components/MainPage";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TourDetail from "./Components/TourDetail";
import { TourFlowProvider } from "./ContextAPI/TourFlowProvider";
import CustomerProfile from "./Components/CustomerProfile";
import AdminPage from "./Components/AdminPage";
import AboutUs from "./Components/AboutUs";
import ContactUs from "./Components/ContactUs";
import UserDataCollection from "./Components/UserDataCollection";
const App = () => {
  return (
    <TourFlowProvider>
      <Router basename="/">
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/tourdetail" element={<TourDetail />} />
          <Route path="/profile" element={<CustomerProfile />} />
          <Route path="/post_tour" element={<AdminPage />} />
          <Route path="/about_us" element={<AboutUs />} />
          <Route path="/contact_us" element={<ContactUs />} />
          <Route
            path="/userdatacollection/:userid"
            element={<UserDataCollection />}
          />
        </Routes>
      </Router>
    </TourFlowProvider>
  );
};

export default App;
