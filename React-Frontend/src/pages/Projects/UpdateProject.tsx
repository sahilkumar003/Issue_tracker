import { useState, useEffect } from "react";
import "./ProjectForm.scss";
import { UpdateCheckBox } from "../../components/Ui/UpdateCheckbox";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import Layout from "../../components/Layout";

export const UpdateProject = () => {
  const { projectId } = useParams();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [users, setUsers] = useState([]);
  const [members, setMembers] = useState([]);
  const [updatedMembers, setUpdatedMembers] = useState([]);

  const API_URL = `${process.env.REACT_APP_BASE_URL}/users/?filter_param=all`;
  const API_URL_MEMBERS = `${process.env.REACT_APP_BASE_URL}/projects/${projectId}/`;
  const navigate = useNavigate();

  const handleUpdateSuccess = () => {
    navigate("/dashboard");
  };

  useEffect(() => {
    const fetchData = async (url) => {
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

    const fetchMembers = async (url) => {
      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        const memberArr = response.data.members;
        setMembers(memberArr);
        setTitle(response.data.title);
        setDescription(response.data.description);
      } catch (err) {
        console.error(err);
      }
    };

    fetchData(API_URL);
    fetchMembers(API_URL_MEMBERS);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.put(
        `${process.env.REACT_APP_BASE_URL}/projects/${projectId}/`,
        {
          description: description,
          updatedMembers: updatedMembers,
        },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );
      handleUpdateSuccess();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Layout>
      <div className="main">
        <div className="header">
          <h2>UPDATE PROJECT</h2>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="input-boxes">
            <div className="form-group">
              <input
                type="title"
                id="title"
                value={title}
                placeholder="Title"
                onChange={(e) => setTitle(e.target.value)}
                style={{ color: "black" }}
                readOnly
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
                style={{ color: "black" }}
                required
              />
            </div>
          </div>

          <div className="checkbox">
            <UpdateCheckBox
              users={users}
              members={members}
              updatedMembers={setUpdatedMembers}
            />
          </div>

          <div className="button">
            <button type="submit" onClick={handleSubmit}>
              Update Project
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};
