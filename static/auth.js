// DOM Elements
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const loginTab = document.querySelector('.auth-tab:nth-child(1)');
const signupTab = document.querySelector('.auth-tab:nth-child(2)');

// Switch between login and signup tabs
function switchAuth(tab) {
  document.querySelectorAll('.auth-tab').forEach(btn => btn.classList.remove('active'));
  
  if (tab === "login") {
    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
    loginTab.classList.add('active');
  } else {
    signupForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    signupTab.classList.add('active');
  }
}

// Form validation helper
function validateForm(form, isLogin = true) {
  const email = form.querySelector('input[type="email"]').value.trim();
  const password = form.querySelector('input[type="password"]').value;
  
  if (!email || !password) {
    showAlert('Please fill in all fields', 'error');
    return false;
  }
  
  if (!/^\S+@\S+\.\S+$/.test(email)) {
    showAlert('Please enter a valid email address', 'error');
    return false;
  }
  
  if (!isLogin) {
    const name = form.querySelector('input[type="text"]').value.trim();
    if (!name) {
      showAlert('Please enter your full name', 'error');
      return false;
    }
    
    if (password.length < 8) {
      showAlert('Password must be at least 8 characters', 'error');
      return false;
    }
  }
  
  return true;
}

// Show loading state on buttons
function setLoading(button, isLoading) {
  if (isLoading) {
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    button.disabled = true;
  } else {
    if (button === loginForm.querySelector('button')) {
      button.textContent = 'Login';
    } else {
      button.textContent = 'Sign Up';
    }
    button.disabled = false;
  }
}

// Show alert notification
function showAlert(message, type) {
  const alert = document.createElement("div");
  alert.className = `alert alert-${type}`;
  alert.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
    ${message}
  `;
  
  document.querySelector('.auth-container').prepend(alert);
  
  setTimeout(() => {
    alert.classList.add("fade-out");
    setTimeout(() => alert.remove(), 500);
  }, 3000);
}

// Add alert styles dynamically
const style = document.createElement("style");
style.textContent = `
  .alert {
    position: relative;
    padding: 12px 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;
document.head.appendChild(style);

// Login form submission
// Login form submission
loginForm.addEventListener("submit", async function(e) {
  e.preventDefault();
  
  if (!validateForm(loginForm)) return;
  
  const button = this.querySelector('button');
  setLoading(button, true);
  
  const formData = new FormData(this);
  
  try {
    const response = await fetch('/login', {
      method: 'POST',
      body: formData
    });
    
    if (response.redirected) {
      window.location.href = response.url;
    }
  } catch (err) {
    showAlert('Login failed', 'error');
  }
  setLoading(button, false);
});
// Signup form submission
signupForm.addEventListener("submit", async function(e) {
  e.preventDefault();
  
  if (!validateForm(signupForm, false)) return;
  
  const button = this.querySelector('button');
  setLoading(button, true);
  
  // Simulate API call with delay
  setTimeout(() => {
    setLoading(button, false);
    showAlert('Account created successfully! Redirecting...', 'success');
    
    // Redirect to dashboard after short delay
    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 1500);
  }, 2000);
});

// Add password toggle functionality
function addPasswordToggle() {
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  
  passwordInputs.forEach(input => {
    const wrapper = document.createElement('div');
    wrapper.className = 'password-wrapper';
    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);
    
    const toggle = document.createElement('span');
    toggle.className = 'password-toggle';
    toggle.innerHTML = '<i class="far fa-eye"></i>';
    wrapper.appendChild(toggle);
    
    toggle.addEventListener('click', () => {
      if (input.type === 'password') {
        input.type = 'text';
        toggle.innerHTML = '<i class="far fa-eye-slash"></i>';
      } else {
        input.type = 'password';
        toggle.innerHTML = '<i class="far fa-eye"></i>';
      }
    });
  });
  
  // Add styles for password toggle
  const toggleStyle = document.createElement('style');
  toggleStyle.textContent = `
    .password-wrapper {
      position: relative;
    }
    
    .password-toggle {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      cursor: pointer;
      color: #6b7280;
    }
    
    .password-toggle:hover {
      color: #4b5563;
    }
  `;
  document.head.appendChild(toggleStyle);
}

// Initialize password toggle
addPasswordToggle();


// Replace the signup form submission handler with:
signupForm.addEventListener("submit", async function(e) {
  e.preventDefault();
  
  if (!validateForm(signupForm, false)) return;

  const button = this.querySelector('button');
  setLoading(button, true);

  try {
      const response = await fetch('/signup', {
          method: 'POST',
          body: new FormData(this)
      });
      
      if (response.redirected) {
          window.location.href = response.url;
      }
  } catch (err) {
      showAlert('Signup failed', 'error');
  }
  setLoading(button, false);
});