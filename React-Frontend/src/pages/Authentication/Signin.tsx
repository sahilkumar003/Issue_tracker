import React, { useState } from "react";
import { AuthComponent } from "./Authcomponent";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { saveAccessToken } from "../../Utils/authUtils";

const Signin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const auth = ["If you don't have an account", "Register here!"];
  const header = "Sign In to";
  const url = "/signup";

  const navigate = useNavigate();

  const handleSignupSuccess = () => {
    navigate("/dashboard");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const data = {
        email: email,
        password: password,
      };
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/signin`,
        data
      );
      saveAccessToken(response.data.access_token);
      handleSignupSuccess();
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <>
      <AuthComponent auth={auth} header={header} url={url} />
      <div className="registration-form">
        <h2>Sign In</h2>
        <form id="formData" onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="email"
              id="email"
              value={email}
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              id="password"
              value={password}
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    </>
  );
};

export default Signin;
