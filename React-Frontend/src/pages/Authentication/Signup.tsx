import React, { useState } from "react";
import axios from "axios";
import { AuthComponent } from "./Authcomponent";
import { useNavigate } from "react-router-dom";
import { saveAccessToken } from "../../Utils/authUtils";

const Signup = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [dob, setDob] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const auth = ["If you already have an account", "Login here!"];
  const header = ["Sign Up to"];
  const url = "/";

  const navigate = useNavigate();

  const handleSignupSuccess = () => {
    navigate("/dashboard");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/signup`,
        {
          first_name: firstName,
          last_name: lastName,
          dob: dob,
          email: email,
          password: password,
          confirm_password: confirmPassword,
        }
      );
      saveAccessToken(response.data.access_token);
      handleSignupSuccess();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDobChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedDate = new Date(e.target.value);
    const currentDate = new Date();

    if (selectedDate > currentDate) {
      e.target.setCustomValidity("Date of birth cannot be in the future");
    } else {
      e.target.setCustomValidity("");
    }

    setDob(e.target.value);
  };

  const handleCofirmPassword = (e: React.ChangeEvent<HTMLInputElement>) => {
    const pass = document.getElementById("password").value;
    const confpass = e.target.value;

    if (confpass !== pass) {
      e.target.setCustomValidity("Password must be same");
    } else {
      e.target.setCustomValidity("");
    }

    setConfirmPassword(e.target.value);
  };

  return (
    <>
      <AuthComponent auth={auth} header={header} url={url} />
      <div className="registration-form">
        <h2>Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              id="firstName"
              value={firstName}
              placeholder="First Name"
              pattern="[A-Za-z]+"
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
            <span className="error-message">
              Name should only contain alphabetical characters
            </span>
          </div>
          <div className="form-group">
            <input
              type="text"
              id="lastName"
              value={lastName}
              placeholder="Last Name"
              pattern="[A-Za-z]+"
              onChange={(e) => setLastName(e.target.value)}
              required
            />
            <span className="error-message">
              Name should only contain alphabetical characters
            </span>
          </div>
          <div className="form-group">
            <input
              className="birth"
              type="date"
              id="dob"
              value={dob}
              onChange={handleDobChange}
            />
            <span className="error-message">
              Date of birth cannot be in the future
            </span>
          </div>
          <div className="form-group">
            <input
              type="email"
              id="email"
              value={email}
              placeholder="Email"
              pattern=".+@gmail\.com"
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <span className="error-message">
              Only emails ending with @gmail.com are allowed
            </span>
          </div>
          <div className="form-group">
            <input
              type="password"
              id="password"
              value={password}
              placeholder="Password"
              pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.*\s).{6,}"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <span className="error-message">
              Password must contain at least one lowercase letter, one uppercase
              letter, one number, one special character, and should be atleast 6
              character long
            </span>
          </div>
          <div className="form-group">
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              placeholder="Confirm Password"
              onChange={handleCofirmPassword}
              required
            />
            <span className="error-message">Password must be same</span>
          </div>
          <button type="submit">Register</button>
        </form>
      </div>
    </>
  );
};

export default Signup;
