document.addEventListener("DOMContentLoaded", () => {
  const registeredUsers = 1500;
  const padsDispensed = 3200;

  
  document.getElementById("registered-users").textContent = `Registered Users: ${registeredUsers}`;
  document.getElementById("pads-dispensed").textContent = `Pads Dispensed: ${padsDispensed}`;

  
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Sep", "Oct", "Nov", "Dec"];
  const userData = [100, 170, 300, 200, 510, 97, 340, 750, 432, 654];

  
  const data = {
    labels: months, 
    datasets: [
      {
        label: "Number of Users",
        data: userData,
        borderColor: "#007bff", 
        backgroundColor: "rgba(0, 123, 255, 0.2)", 
        borderWidth: 3, 
        fill: true, 
        tension: 0, 
        pointBackgroundColor: "#fff", 
        pointBorderColor: "#007bff", 
        pointRadius: 5, 
      },
    ],
  };

  
  const config = {
    type: "line",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true, 
          position: "top", 
        },
        tooltip: {
          enabled: true, 
          callbacks: {
            label: (context) => `Users: ${context.raw}`, 
          },
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Months", 
            color: "#333",
            font: {
              size: 14,
              weight: "bold",
            },
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Users Count", 
            color: "#333",
            font: {
              size: 14,
              weight: "bold",
            },
          },
          grid: {
            color: "rgba(200, 200, 200, 0.5)", 
            borderDash: [5, 5], 
          },
        },
      },
    },
  };

 
  const ctx = document.getElementById("usageChart").getContext("2d");
  new Chart(ctx, config);
});
