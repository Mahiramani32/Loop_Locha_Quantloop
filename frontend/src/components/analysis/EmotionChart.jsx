import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

const EmotionChart = ({ data }) => {
  // Generate labels based on actual data length (one point per episode)
  const dataLength = data.joy?.length || 5;
  const chartLabels = Array.from({ length: dataLength }, (_, i) => `Ep ${i + 1}`);

  const chartData = {
    labels: chartLabels.slice(0, data.joy?.length || 5),
    datasets: [
      {
        label: "Joy",
        data: data.joy || [],
        borderColor: "rgb(255, 205, 86)",
        backgroundColor: "rgba(255, 205, 86, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Sadness",
        data: data.sadness || [],
        borderColor: "rgb(54, 162, 235)",
        backgroundColor: "rgba(54, 162, 235, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Anger",
        data: data.anger || [],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Fear",
        data: data.fear || [],
        borderColor: "rgb(153, 102, 255)",
        backgroundColor: "rgba(153, 102, 255, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Surprise",
        data: data.surprise || [],
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.1)",
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default EmotionChart;
