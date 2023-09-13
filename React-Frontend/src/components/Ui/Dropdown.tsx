export const GenericDropdownList = ({
  items,
  selectedItem,
  setSelectedItem,
  label,
}) => {
  const handleOptionChange = (e) => {
    setSelectedItem(e.target.value);
  };

  return (
    <div className="App">
      <br />
      <label htmlFor="dropdown" className="label-assign">
        {label}
      </label>
      <br />
      <select
        onChange={handleOptionChange}
        id="dropdown-options"
        value={selectedItem || ""}
      >
        {items.map(({ id, value }) => (
          <option key={id} value={id}>
            {value}
          </option>
        ))}
      </select>
    </div>
  );
};
