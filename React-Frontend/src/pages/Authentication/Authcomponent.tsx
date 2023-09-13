import "./Auth.scss";
import pic from "../../assets/Saly-15.svg";
import { useNavigate } from "react-router-dom";

export function AuthComponent(props) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(props.url);
  };

  return (
    <div className="leftside">
      <div className="text">
        <p>ISSUE TRACKER SYSTEM</p>
      </div>

      <div className="imagediv">
        <div className="headingtext">
          <div className="toptext">
            <p>
              <span className="text1">{props.header}</span>
              <br /> <span className="text2">Issue Tracker System</span>
            </p>
          </div>
          <div className="bottomtext">
            <p>
              <span className="text3">{props.auth[0]}</span>
              <br /> <span className="text5"> You can </span>
              <span className="text4" onClick={handleClick}>
                {props.auth[1]}
              </span>
            </p>
          </div>
        </div>
        <img src={pic} alt="image" />
      </div>
    </div>
  );
}
