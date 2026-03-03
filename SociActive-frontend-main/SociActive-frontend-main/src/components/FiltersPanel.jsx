// src/components/FiltersPanel.jsx
import React, { useState } from "react";
import "./FiltersPanel.css";

// Reusable Accordion Section Component
const AccordionSection = ({ title, isOpen, onToggle, children }) => (
  <div className="accordion-section">
    <div className="accordion-header" onClick={onToggle}>
      <span>{title}</span>
      <span>{isOpen ? "▲" : "▼"}</span>
    </div>
    {isOpen && <div className="accordion-body">{children}</div>}
  </div>
);

// Reusable Radio Group Component
const RadioGroup = ({ name, options, value, onChange }) => (
  <>
    {options.map((option) => (
      <label key={option} className="radio-item">
        <input
          type="radio"
          name={name}
          checked={value === option}
          onChange={() => onChange(name, option)}
        />
        {option}
      </label>
    ))}
    <label className="radio-item">
      <input
        type="radio"
        name={name}
        checked={!value}
        onChange={() => onChange(name, "")}
      />
      All
    </label>
  </>
);

const FiltersPanel = ({ initialFilters, onApply, onClose }) => {
  const [filters, setFilters] = useState(initialFilters || {});

  const [open, setOpen] = useState({
    type: true,
    date: true,
    location: true,
    participants: true,
    difficulty: true,
  });

  const toggleSection = (key) =>
    setOpen((prev) => ({ ...prev, [key]: !prev[key] }));

  const handleRadio = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const updateFilter = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const clearFilters = () => {
    onApply({});
    onClose();
  };

  const apply = () => {
    onApply(filters);
    onClose();
  };

  return (
    <div className="filters-panel-inline">
      <div className="panel-header">
        <h3>Filters</h3>
        <button className="apply-btn-top" onClick={apply}>
          Apply
        </button>
      </div>

      {/* TYPE */}
      <AccordionSection
        title="Type"
        isOpen={open.type}
        onToggle={() => toggleSection("type")}
      >
        <RadioGroup
          name="type"
          options={[
            "Running",
            "Hiking",
            "Walking",
            "Rock climbing",
            "Mountain biking",
            "Beach Volley",
          ]}
          value={filters.type}
          onChange={handleRadio}
        />
      </AccordionSection>

      {/* DATE */}
      <AccordionSection
        title="Date"
        isOpen={open.date}
        onToggle={() => toggleSection("date")}
      >
        <label>From:</label>
        <input
          type="date"
          value={filters.dateFrom || ""}
          onChange={(e) => updateFilter("dateFrom", e.target.value)}
        />
        <label>To:</label>
        <input
          type="date"
          value={filters.dateTo || ""}
          onChange={(e) => updateFilter("dateTo", e.target.value)}
        />
      </AccordionSection>

      {/* LOCATION */}
      <AccordionSection
        title="Location"
        isOpen={open.location}
        onToggle={() => toggleSection("location")}
      >
        <RadioGroup
          name="location"
          options={["Athens", "Patras", "Thessaloniki", "Ioannina"]}
          value={filters.location}
          onChange={handleRadio}
        />
      </AccordionSection>

      {/* PARTICIPANTS */}
      <AccordionSection
        title="Participants"
        isOpen={open.participants}
        onToggle={() => toggleSection("participants")}
      >
        <input
          type="range"
          min="1"
          max="20"
          value={filters.participants || 10}
          onChange={(e) => updateFilter("participants", e.target.value)}
        />
        <div>Selected: {filters.participants || 10}</div>
      </AccordionSection>

      {/* DIFFICULTY */}
      <AccordionSection
        title="Level of difficulty"
        isOpen={open.difficulty}
        onToggle={() => toggleSection("difficulty")}
      >
        <RadioGroup
          name="difficulty"
          options={["Beginner", "Intermediate", "Advanced"]}
          value={filters.difficulty}
          onChange={handleRadio}
        />
      </AccordionSection>

      <button className="clear-btn" onClick={clearFilters}>
        Clear filters
      </button>
    </div>
  );
};

export default FiltersPanel;
