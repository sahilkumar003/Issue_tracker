import { useState, useEffect } from "react";

export const UpdateCheckBox = ({ users, members, updatedMembers }) => {
  const [ids, setIds] = useState([]);

  useEffect(() => {
    const newArr = members.map((member) => {
      return member.id;
    });
    setIds(newArr);
    updatedMembers(newArr);
  }, [members]);

  const selectUser = (event) => {
    const selectedId = parseInt(event.target.value);

    if (ids.includes(selectedId)) {
      const newIds = ids.filter((id) => id !== selectedId);
      setIds(newIds);
      updatedMembers(newIds);
    } else {
      const newIds = [...ids];
      newIds.push(selectedId);
      setIds(newIds);
      updatedMembers(newIds);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Add Members:</h2>
      {users.length === 0 && <h3>Loading...</h3>}
      {users.length > 0 &&
        users.map((user) => (
          <div style={styles.userItem} key={user.email}>
            <span style={styles.userName}>{user.first_name}</span>
            <span style={styles.userCheckbox}>
              <input
                type="checkbox"
                value={user.id}
                onChange={selectUser}
                checked={ids.includes(user.id) ? true : false}
              />
            </span>
          </div>
        ))}
    </div>
  );
};

const styles = {
  container: {
    width: 500,
    margin: "10px auto",
    display: "flex",
    flexDirection: "column",
  },
  userItem: {
    width: "100%",
    display: "flex",
    justifyContent: "space-between",
    margin: "6px 0",
    padding: "8px 15px",
    backgroundColor: " #F0EFFF",
  },
  userId: {
    width: "5%",
  },
  userName: {
    width: "30%",
  },
  userEmail: {
    width: "40%",
  },
};
