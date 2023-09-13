import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./UserProfile.scss";
import Layout from "../../components/Layout";
const UserProfile = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [dob, setDob] = useState("");
  const [email, setEmail] = useState("");
  const [userId, setuserId] = useState<number | undefined>();
  const navigate = useNavigate();
  const handleChangesSuccess = () => {
    navigate("/dashboard");
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BASE_URL}/users/current`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        setFirstName(response.data.first_name);
        setLastName(response.data.last_name);
        setDob(response.data.dob);
        setEmail(response.data.email);
        setuserId(response.data.id);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, []);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.patch(
        `${process.env.REACT_APP_BASE_URL}/users/${userId}/`,
        {
          first_name: firstName,
          last_name: lastName,
          dob: dob,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      handleChangesSuccess();
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
  return (
    <Layout>
      <div className="main1">
        <div className="registration-form1">
          <h2>Profile</h2>
          <form id="formData" onSubmit={handleSubmit}>
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
                readOnly
              />
            </div>
            <button type="submit">Save Changes</button>
          </form>
        </div>
      </div>
    </Layout>
  );
};
export default UserProfile;
