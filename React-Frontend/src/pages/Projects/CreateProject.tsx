import React, { useState, useEffect } from "react";
import "./ProjectForm.scss";
import { CheckBox } from "../../components/Ui/CheckBox";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Layout from "../../components/Layout";

let API_URL = `${process.env.REACT_APP_BASE_URL}/users/`;

interface User {
  id: number;
  first_name: string;
  email: string;
  last_name: string;
  dob: Object;
  password: string;
}

export const CreateProject = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [users, setUsers] = useState<Array<User>>([]);
  const [potentialMembers, setPotentialMembers] = useState<Array<User>>([]);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  const handleSignupSuccess = () => {
    navigate("/dashboard");
  };
  const handleSearch = (e) => {
    setSearch(e.target.value);
  };

  useEffect(() => {
    const fetchData = async (url: string) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        setUsers(response.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData(API_URL);
  }, []);

  useEffect(() => {
    API_URL = `${process.env.REACT_APP_BASE_URL}/users/?search=${search}`;
    const fetchData = setTimeout(() => {
      try {
        const promise = axios
          .get(API_URL, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          })
          .then((res) => {
            setUsers(res.data);
          });
      } catch (err) {
        console.error(err);
      }
    }, 1000);

    return () => clearTimeout(fetchData);
  }, [search]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL}/projects/`,
        {
          title: title,
          description: description,
          members: potentialMembers,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );
      handleSignupSuccess();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Layout>
      <div className="main">
        <div className="header">
          <h2>Create Project</h2>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="title"
              id="title"
              value={title}
              placeholder="Title"
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="text"
              id="desciption"
              value={description}
              placeholder="Description"
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <h2>Add Members:</h2>
          <input
            type="text"
            placeholder="Search Members"
            onChange={handleSearch}
          ></input>
          <div className="checkbox">
            <CheckBox users={users} setPotentialMembers={setPotentialMembers} />
          </div>

          <div className="button">
            <button type="submit" onClick={handleSubmit}>
              Add Project
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};
