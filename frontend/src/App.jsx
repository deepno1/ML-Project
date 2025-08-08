import { useState } from "react";

export default function App() {
  const [form, setForm] = useState({
    gender: "male",
    race_ethnicity: "group A",
    parental_level_of_education: "high school",
    lunch: "standard",
    test_preparation_course: "none",
    reading_score: 50,
    writing_score: 50,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleRangeChange = (name, value) => {
    setForm({ ...form, [name]: Number(value) });
  };

  const handleSubmit = async () => {
  setLoading(true);
  setError(null);
  setPrediction(null);

  try {
  const response = await fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(form)
  });
  if (!response.ok) throw new Error('Network response was not ok');
  const data = await response.json();
  setPrediction(data.math_score);
} catch (err) {
  setError("Prediction failed");
} finally {
  setLoading(false);
}

  };


  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-purple-200 to-pink-200">
      <div className="bg-white p-8 rounded-3xl shadow-xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">
          🎓 Student Math Score Predictor
        </h1>

        {/* Gender */}
        <label className="block mb-2 font-medium">Gender</label>
        <select
          name="gender"
          value={form.gender}
          onChange={handleChange}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="male">male</option>
          <option value="female">female</option>
        </select>

        {/* Race Ethnicity */}
        <label className="block mb-2 font-medium">Race Ethnicity</label>
        <select
          name="race_ethnicity"
          value={form.race_ethnicity}
          onChange={handleChange}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="group A">group A</option>
          <option value="group B">group B</option>
          <option value="group C">group C</option>
          <option value="group D">group D</option>
          <option value="group E">group E</option>
        </select>

        {/* Parental level of education */}
        <label className="block mb-2 font-medium">Parental level of education</label>
        <select
          name="parental_level_of_education"
          value={form.parental_level_of_education}
          onChange={handleChange}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="high school">high school</option>
          <option value="some college">some college</option>
          <option value="bachelor's degree">bachelor's degree</option>
          <option value="master's degree">master's degree</option>
          <option value="associate's degree">associate's degree</option>
          <option value="some high school">some high school</option>
        </select>

        {/* Lunch */}
        <label className="block mb-2 font-medium">Lunch</label>
        <select
          name="lunch"
          value={form.lunch}
          onChange={handleChange}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="standard">standard</option>
          <option value="free/reduced">free/reduced</option>
        </select>

        {/* Test preparation course */}
        <label className="block mb-2 font-medium">Test preparation course</label>
        <select
          name="test_preparation_course"
          value={form.test_preparation_course}
          onChange={handleChange}
          className="w-full p-2 border rounded-lg mb-4"
        >
          <option value="none">none</option>
          <option value="completed">completed</option>
        </select>

        {/* Reading Score */}
        <label className="block mb-2 font-medium">Reading score</label>
        <input
          type="range"
          min="0"
          max="100"
          value={form.reading_score}
          onChange={(e) => handleRangeChange("reading_score", e.target.value)}
          className="w-full accent-blue-500 mb-2"
        />
        <div className="text-center mb-4">{form.reading_score}</div>

        {/* Writing Score */}
        <label className="block mb-2 font-medium">Writing score</label>
        <input
          type="range"
          min="0"
          max="100"
          value={form.writing_score}
          onChange={(e) => handleRangeChange("writing_score", e.target.value)}
          className="w-full accent-blue-500 mb-2"
        />
        <div className="text-center mb-4">{form.writing_score}</div>

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-xl transition"
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict Math Score"}
        </button>

        {prediction !== null && (
          <div className="mt-6 text-center text-xl font-semibold text-green-600">
            Predicted Math Score: {prediction}
          </div>
        )}

        {error && (
          <div className="mt-6 text-center text-red-600 font-medium">{error}</div>
        )}
      </div>
    </div>
  );
}
