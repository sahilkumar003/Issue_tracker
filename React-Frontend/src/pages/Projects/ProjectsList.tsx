import { useState, useEffect } from "react";
import axios from "axios";
import "./Projects.scss";
import { ProjectView } from "./dashboard";
import Layout from "../../components/Layout";

export function Projects() {
  const [projects, setProjects] = useState([]);
  const [filterValue, setFilterValue] = useState("all");

  const handleFilter = (e) => {
    setFilterValue(e.target.value);
  };

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_BASE_URL}/projects/?filter_param=${filterValue}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        setProjects(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchProjects();
  }, [filterValue]);

  return (
    <Layout>
      <div className="main-container">
        <div className="container mt-4">
          <div className="row">
            <div className="col-md-6">
              <h1 className="text-center">Dashboard</h1>
            </div>
          </div>

          <div className="row mt-4">
            <div className="col-md-12">
              <select
                id="projectFilter"
                className="select"
                autoFocus
                onChange={(e) => {
                  handleFilter(e);
                }}
              >
                <option value="all">All Projects</option>
                <option value="owned">Owned Projects</option>
                <option value="member">Member Projects</option>
              </select>
            </div>
          </div>
          <div className="col-md-12">
            <h2>Projects</h2>
          </div>

          {projects.map((project) => (
            <ProjectView key={project.id} project={project} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
