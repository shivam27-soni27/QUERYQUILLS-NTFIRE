const uploadButton = document.querySelector(".upload-btn");
const progressBar = document.getElementById("progress-bar");
const fileNameSpan = document.querySelector(".file-name");
const fileInput = document.getElementById("file-input");

// Trigger file input click when the upload button is clicked
uploadButton.addEventListener("click", () => {
  fileInput.click();
});

// Event listener for file input change
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    // Check if the uploaded file is a CSV file
    if (file.type === "text/csv" || file.name.endsWith(".csv")) {
      fileNameSpan.textContent = file.name;
      uploadFile(file);
    } else {
      fileNameSpan.textContent =
        "Invalid file format. Please upload a CSV file.";
      fileInput.value = ""; // Clear the file input
    }
  } else {
    fileNameSpan.textContent = "No file chosen";
  }
});

// Function to upload the file
function uploadFile(file) {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "your-upload-url", true);
  xhr.upload.onprogress = (e) => {
    const percent = (e.loaded / e.total) * 100;
    progressBar.style.width = percent + "%";
  };

  xhr.onload = () => {
    if (xhr.status === 200) {
      console.log("File uploaded successfully");
      progressBar.style.width = "0%";
    } else {
      console.error("Error uploading file");
    }
  };

  xhr.onerror = () => {
    console.error("Error uploading file");
  };

  const formData = new FormData();
  formData.append("file", file);
  xhr.send(formData);
}

document.querySelector(".login-btn").addEventListener("click", function () {
  window.location.href = "/login";
});

executeButton.onclick = function () {
  const query = searchInput.value.trim();
  if (query !== "") {
      fetch('/process_form/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': '{{ csrf_token }}'  // Add CSRF token if CSRF protection is enabled
          },
          body: JSON.stringify({query: query})
      })
      .then(response => response.json())
      .then(data => {
          if (data.result) {
              outputDiv.innerHTML = `<h3><i class="fas fa-arrow-alt-circle-left"></i> Output:</h3><p>${JSON.stringify(data.result)}</p>`;
          } else {
              outputDiv.innerHTML = '<p>Error executing SQL query.</p>';
          }
      })
      .catch(error => {
          console.error('Error:', error);
          outputDiv.innerHTML = '<p>Error executing SQL query.</p>';
      });

      executeButton.disabled = true;
      searchInput.focus();
      container.removeChild(executeButton);
   
      searchInput.value = "";

      inputOutputBox.scrollTop = inputOutputBox.scrollHeight;
  }
};


  // Function to execute SQL query
  function executeSQL(sqlQuery, outputDiv) {
    // Simulate execution and display output under the corresponding response
    const output = "Output for SQL query: " + sqlQuery;
    const outputP = document.createElement("p");
    outputP.innerHTML = `<i class="fas fa-database"></i> ${output}`; // Replace text with icon
    outputDiv.appendChild(outputP);
  }

  // Add event listener for Enter key press in the input field
  searchForm.addEventListener("submit", function (event) {
    event.preventDefault(); 
  });
});
