import "../styles/ModalBookTour.css";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import React from "react";
import { useStringContext } from "../ContextAPI/TourFlowProvider";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ModalBookTour: React.FC<ModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;
  const { setLogin } = useStringContext();

  const handleLoginSuccess = (response: any) => {
    console.log("response: ", response);
    const tokenId = response.credential;
    fetch("http://localhost:5175/api/auth/google-signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        idToken: tokenId,
      }),
    })
      .then((responsefromBE) => {
        if (!responsefromBE.ok) {
          throw new Error("Failed to submit data");
        }
        return responsefromBE.json(); // Return the Promise from response.json()
      })
      .then((res) => {
        console.log("res: ", res);
        sessionStorage.setItem("id", res.id);
        sessionStorage.setItem("jwt", res.jwt);
        sessionStorage.setItem("refreshToken", res.refreshToken);
        sessionStorage.setItem("name", res.name);
        sessionStorage.setItem("avaUrl", res.avaUrl);
        if (res.role == true) {
          sessionStorage.setItem("isAdmin", "1");
        } else {
          console.log("something went wrong in role dcm");
        }
        if (sessionStorage.getItem("jwt")) {
          setLogin(true);
        }
      })
      .catch((error) => {
        console.log("Exception occurred: ", error);
      });
  };

  const handleLoginFailure = () => {
    console.log("Login failed ");
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-container">
        <div className="modal-content">
          <button className="close-button" onClick={onClose}>
            &times;
          </button>
          <div className="flex-item item-1">
            <img
              id="logo-nav-bar"
              src="src/Imgs/companyLogo.png"
              alt="Company Logo"
            />
          </div>
          <h5>Sign in for booking our tour</h5>
          <GoogleOAuthProvider clientId="979412040830-vcasa58bqundafvangterge2artb5kqk.apps.googleusercontent.com">
            <div className="google-login-container">
              <GoogleLogin
                onSuccess={handleLoginSuccess}
                onError={handleLoginFailure}
              />
            </div>
          </GoogleOAuthProvider>
        </div>
      </div>
    </div>
  );
};

export default ModalBookTour;
