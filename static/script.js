// Dashboard Functions
function addStudent() {
    const name = document.getElementById("studentName").value;
    const photo = document.getElementById("studentPhoto").files[0];
  
    if (!name || !photo) {
      showAlert("Please enter a name and select a photo.", "error");
      return;
    }
  
    // Show loading state
    const button = document.querySelector('#add button');
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    
    // Simulate API call
    setTimeout(() => {
      showAlert(`Student "${name}" added successfully!`, "success");
      document.getElementById("studentName").value = "";
      document.getElementById("studentPhoto").value = "";
      button.innerHTML = '<i class="fas fa-save"></i> Save Student';
      
      // Add to logs
      const logList = document.getElementById("logList");
      const logEntry = document.createElement("li");
      logEntry.innerHTML = `
        <i class="fas fa-user-plus info-icon"></i>
        <span>New student "${name}" added</span>
        <span class="log-time">Just now</span>
      `;
      logList.prepend(logEntry);
    }, 1500);
  }
  
//   function markAttendance() {
//     const photo = document.getElementById("attendancePhoto").files[0];
  
//     if (!photo) {
//       showAlert("Please select a class photo.", "error");
//       return;
//     }
  
//     // Show loading state
//     const button = document.querySelector('#mark button');
//     button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
//     const resultDiv = document.getElementById("attendanceResult");
//     resultDiv.innerHTML = `<p><i class="fas fa-spinner fa-spin"></i> Recognizing faces...</p>`;
  
//     // Simulate API call with delay
//     setTimeout(() => {
//       resultDiv.innerHTML = `
//         <div class="attendance-success">
//           <i class="fas fa-check-circle success-icon"></i>
//           <h4>Attendance Marked Successfully!</h4>
//         </div>
//         <div class="attendance-details">
//           <div class="detail-item">
//             <span>Date:</span>
//             <span>${new Date().toLocaleDateString()}</span>
//           </div>
//           <div class="detail-item">
//             <span>Time:</span>
//             <span>${new Date().toLocaleTimeString()}</span>
//           </div>
//           <div class="detail-item">
//             <span>Students Present:</span>
//             <span>15/20</span>
//           </div>
//         </div>
//         <ul class="attendance-list">
//           <li><i class="fas fa-check success-icon"></i> Alice Johnson</li>
//           <li><i class="fas fa-check success-icon"></i> Bob Smith</li>
//           <li><i class="fas fa-times danger-icon"></i> Charlie Brown (Absent)</li>
//         </ul>
//       `;
//       button.innerHTML = '<i class="fas fa-search"></i> Recognize Faces';
  
//       // Add to logs
//       const logList = document.getElementById("logList");
//       const logEntry = document.createElement("li");
//       logEntry.innerHTML = `
//         <i class="fas fa-check-circle success-icon"></i>
//         <span>Attendance marked (15/20 present)</span>
//         <span class="log-time">Just now</span>
//       `;
//       logList.prepend(logEntry);
//     }, 2000);
//   }

function markAttendance() {
  const photo = document.getElementById("attendancePhoto").files[0];

  if (!photo) {
      showAlert("Please select a class photo.", "error");
      return;
  }

  const button = document.querySelector('#mark button');
  button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
  const resultDiv = document.getElementById("attendanceResult");
  resultDiv.innerHTML = `<p><i class="fas fa-spinner fa-spin"></i> Recognizing faces...</p>`;

  const formData = new FormData();
  formData.append("photo", photo);

  fetch("http://localhost:5000/recognize", {
      method: "POST",
      body: formData
  })
  .then(res => res.json())
  .then(data => {
      resultDiv.innerHTML = `
          <h4>Attendance Results (${data.recognized_count}/${data.total_students})</h4>
          <div class="attendance-stats">
              <span class="success">Recognized: ${data.recognized_count}</span>
              <span class="danger">Unknown: ${data.unknown_count}</span>
          </div>
          <ul class="attendance-list">
      `;

      data.faces.forEach(face => {
          const icon = face.status === 'recognized' ? 
              'check success-icon' : 'times danger-icon';
          resultDiv.innerHTML += `
              <li>
                  <i class="fas fa-${icon}"></i>
                  ${face.label} ${face.status === 'recognized' ? `(${face.confidence}%)` : ''}
              </li>
          `;

          // Show popup for recognized students
          if (face.status === 'recognized') {
              showAlert(`Attendance for ${face.label} marked!`, 'success');
          }
      });

      resultDiv.innerHTML += `</ul>`;
      button.innerHTML = '<i class="fas fa-search"></i> Recognize Faces';

      // Add to logs
      const logEntry = document.createElement("li");
      logEntry.innerHTML = `
          <i class="fas fa-check-circle success-icon"></i>
          <span>Attendance marked (${data.recognized_count}/${data.total_students} present)</span>
          <span class="log-time">Just now</span>
      `;
      document.getElementById("logList").prepend(logEntry);
  })
  .catch(err => {
      console.error("Error:", err);
      showAlert("Recognition failed. Try again.", "error");
      button.innerHTML = '<i class="fas fa-search"></i> Recognize Faces';
      resultDiv.innerHTML = "";
  });
  
}











  
  function deleteStudent() {
    const studentSelect = document.getElementById("studentList");
    const selectedStudent = studentSelect.options[studentSelect.selectedIndex];
    
    if (!selectedStudent.value) {
      showAlert("Please select a student to delete.", "error");
      return;
    }
  
    if (confirm(`Are you sure you want to delete ${selectedStudent.text}? This cannot be undone.`)) {
      const button = document.querySelector('#delete button');
      button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
      
      // Simulate API call
      setTimeout(() => {
        showAlert(`Student "${selectedStudent.text}" deleted successfully.`, "success");
        button.innerHTML = '<i class="fas fa-trash"></i> Delete Student';
        
        // Add to logs
        const logList = document.getElementById("logList");
        const logEntry = document.createElement("li");
        logEntry.innerHTML = `
          <i class="fas fa-trash danger-icon"></i>
          <span>Student "${selectedStudent.text}" removed</span>
          <span class="log-time">Just now</span>
        `;
        logList.prepend(logEntry);
        
        // Remove from dropdown (in a real app, this would come from the server)
        studentSelect.remove(studentSelect.selectedIndex);
      }, 1500);
    }
  }
  
  // Single, properly working logout function
  function logout() {
    // Show confirmation dialog with better styling
    const confirmed = confirm("Are you sure you want to logout?");
    if (confirmed) {
      // Show loading state on logout button
      const logoutBtn = document.querySelector('.logout-button');
      const originalHtml = logoutBtn.innerHTML;
      logoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging out...';
      
      // Simulate logout process
      setTimeout(() => {
        // Clear any user data from localStorage/session if needed
        localStorage.removeItem('authToken');
        sessionStorage.clear();
        
        // Redirect to login page
        window.location.href = "index.html";
      }, 1000);
    }
  }
  
  // Alert notification system
  function showAlert(message, type) {
    const alert = document.createElement("div");
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
      <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
      ${message}
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
      alert.classList.add("fade-out");
      setTimeout(() => alert.remove(), 500);
    }, 3000);
  }
  
  // Initialize alert styles if not already present
  if (!document.getElementById('alert-styles')) {
    const style = document.createElement("style");
    style.id = 'alert-styles';
    style.textContent = `
      .alert {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
      }
      
      .alert-success {
        background-color: #d1fae5;
        color: #065f46;
        border-left: 4px solid #10b981;
      }
      
      .alert-error {
        background-color: #fee2e2;
        color: #b91c1c;
        border-left: 4px solid #ef4444;
      }
      
      .fade-out {
        animation: fadeOut 0.5s ease-out forwards;
      }
      
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      
      @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
  
  // Make sure logout button is properly connected (fallback)
  document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.querySelector('.logout-button');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', logout);
    }
  });