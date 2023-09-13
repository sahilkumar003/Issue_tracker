import "./Footer.scss";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { getAccessToken } from "../../Utils/authUtils";
import { removeAccessToken } from "../../Utils/authUtils";

const Footer = () => {
  const logout = async () => {
    try {
      await axios.get(`${process.env.REACT_APP_BASE_URL}/signout`, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
      });
      removeAccessToken();
    } catch (error) {
      console.error(error);
    }
  };

  const navigate = useNavigate();
  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <footer className="footer">
      <div className="footer-text">
        <p>&copy; 2023 Issue Tracker System. All rights reserved.</p>
      </div>
      <div className="btn">
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>
    </footer>
  );
};

export default Footer;
