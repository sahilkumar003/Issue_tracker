import React, { useState } from "react";

export const CheckBox = ({ users, setPotentialMembers }) => {
  const [ids, setIds] = useState<Array<number>>([]);
  // This function will be triggered when a checkbox changes its state
  const selectUser = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedId = parseInt(event.target.value);

    // Check if "ids" contains "selectedIds"
    // If true, this checkbox is already checked
    // Otherwise, it is not selected yet
    if (ids.includes(selectedId)) {
      const newIds = ids.filter((id) => id !== selectedId);
      setIds(newIds);
      setPotentialMembers(newIds);
    } else {
      const newIds = [...ids];
      newIds.push(selectedId);
      setIds(newIds);
      setPotentialMembers(newIds);
    }
  };

  return (
    <div style={styles.container}>
      

      {users.length > 0 &&
        users.map((user) => (
          <div style={styles.userItem} key={user.email}>
            {/* <span style={styles.userId}>{user.id}</span> */}
            <span style={styles.userName}>{user.first_name}</span>
            {/* <span style={styles.userEmail}>{user.email}</span> */}
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

const styles: { [key: string]: React.CSSProperties } = {
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
