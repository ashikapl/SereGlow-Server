// Global variables
let currentUser = null;
let services = [
  {
    id: 1,
    name: "Haircut & Style",
    description: "Professional haircut with styling",
    price: 45,
    duration: 60,
  },
  {
    id: 2,
    name: "Hair Coloring",
    description: "Full hair color treatment",
    price: 85,
    duration: 120,
  },
  {
    id: 3,
    name: "Facial Treatment",
    description: "Deep cleansing facial",
    price: 65,
    duration: 90,
  },
  {
    id: 4,
    name: "Manicure",
    description: "Complete nail care and polish",
    price: 35,
    duration: 45,
  },
  {
    id: 5,
    name: "Pedicure",
    description: "Foot spa and nail treatment",
    price: 40,
    duration: 50,
  },
];
let appointments = [];
let feedbacks = [];
let users = [
  {
    id: 1,
    type: "admin",
    firstName: "Admin",
    lastName: "User",
    email: "admin@salon.com",
    password: "admin123",
    phone: "555-0001",
    address: "123 Beauty Street, Style City, SC 12345",
  },
  {
    id: 2,
    type: "user",
    firstName: "John",
    lastName: "Doe",
    email: "john@example.com",
    password: "user123",
    phone: "555-0002",
    address: "456 User Lane, City, ST 67890",
    username: "JOHN001",
  },
];
let nextUserId = 3;
let nextServiceId = 6;
let nextAppointmentId = 1;

// Navigation
document.getElementById("hamburger").addEventListener("click", function () {
  const navMenu = document.getElementById("navMenu");
  navMenu.classList.toggle("active");
});

// Modal functions
function showLoginModal() {
  document.getElementById("loginModal").style.display = "block";
}

function showSignupModal() {
  document.getElementById("signupModal").style.display = "block";
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

function switchModal(fromModal, toModal) {
  closeModal(fromModal);
  document.getElementById(toModal).style.display = "block";
}

// Authentication
document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const userType = document.getElementById("loginUserType").value;
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  const user = users.find(
    (u) => u.email === email && u.password === password && u.type === userType
  );

  if (user) {
    currentUser = user;
    closeModal("loginModal");
    showDashboard(user.type);
    showNotification("Login successful!", "success");
  } else {
    showNotification("Invalid credentials!", "error");
  }
});

document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const userType = document.getElementById("signupUserType").value;
  const firstName = document.getElementById("signupFirstName").value;
  const lastName = document.getElementById("signupLastName").value;
  const email = document.getElementById("signupEmail").value;
  const phone = document.getElementById("signupPhone").value;
  const address = document.getElementById("signupAddress").value;
  const password = document.getElementById("signupPassword").value;
  const confirmPassword = document.getElementById(
    "signupConfirmPassword"
  ).value;

  if (password !== confirmPassword) {
    showNotification("Passwords do not match!", "error");
    return;
  }

  if (users.find((u) => u.email === email)) {
    showNotification("Email already exists!", "error");
    return;
  }

  let username = "";
  if (userType === "user") {
    username = (firstName.toUpperCase() + "00" + nextUserId).slice(0, 10);
  }

  const newUser = {
    id: nextUserId++,
    type: userType,
    firstName,
    lastName,
    email,
    password,
    phone,
    address,
    username,
  };

  users.push(newUser);
  closeModal("signupModal");
  showNotification("Account created successfully!", "success");
});

// Dashboard functions
function showDashboard(userType) {
  document.getElementById("mainContent").style.display = "none";
  document.querySelector(".navbar").style.display = "none";
  document.querySelector(".footer").style.display = "none";

  if (userType === "admin") {
    document.getElementById("adminDashboard").style.display = "block";
    document.getElementById(
      "adminWelcome"
    ).textContent = `Welcome, ${currentUser.firstName}!`;
    loadAdminData();
    showAdminSection("overview");
  } else {
    document.getElementById("userDashboard").style.display = "block";
    document.getElementById(
      "userWelcome"
    ).textContent = `Welcome, ${currentUser.firstName}!`;
    loadUserData();
    showUserSection("services");
  }
}

function logout() {
  currentUser = null;
  document.getElementById("adminDashboard").style.display = "none";
  document.getElementById("userDashboard").style.display = "none";
  document.getElementById("mainContent").style.display = "block";
  document.querySelector(".navbar").style.display = "block";
  document.querySelector(".footer").style.display = "block";
  showNotification("Logged out successfully!", "success");
}

// Admin Dashboard Functions
function showAdminSection(section) {
  // Hide all sections
  document
    .querySelectorAll("#adminDashboard .dashboard-section")
    .forEach((s) => (s.style.display = "none"));

  // Remove active class from all menu items
  document
    .querySelectorAll("#adminDashboard .sidebar-menu a")
    .forEach((a) => a.classList.remove("active"));

  // Show selected section
  document.getElementById(
    "admin" + section.charAt(0).toUpperCase() + section.slice(1) + "Section"
  ).style.display = "block";

  // Add active class to selected menu item
  event.target.classList.add("active");
}

function loadAdminData() {
  updateAdminStats();
  loadAdminServices();
  loadAdminAppointments();
  loadAdminFeedback();
  loadAdminProfile();
}

function updateAdminStats() {
  document.getElementById("totalAppointments").textContent =
    appointments.length;
  document.getElementById("totalServices").textContent = services.length;
  document.getElementById("totalUsers").textContent = users.filter(
    (u) => u.type === "user"
  ).length;

  const avgRating =
    feedbacks.length > 0
      ? (
          feedbacks.reduce((sum, f) => sum + f.rating, 0) / feedbacks.length
        ).toFixed(1)
      : "0";
  document.getElementById("avgRating").textContent = avgRating;
}

function loadAdminServices() {
  const container = document.getElementById("adminServicesList");
  container.innerHTML = services
    .map(
      (service) => `
                <div class="service-card">
                    <div class="service-header">
                        <h3>${service.name}</h3>
                        <div class="service-actions">
                            <button class="btn-icon" onclick="editService(${service.id})" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn-icon delete" onclick="deleteService(${service.id})" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    <p class="service-description">${service.description}</p>
                    <div class="service-details">
                        <span class="service-price">${service.price}</span>
                        <span class="service-duration">${service.duration} min</span>
                    </div>
                </div>
            `
    )
    .join("");
}

function loadAdminAppointments() {
  const filter = document.getElementById("appointmentFilter")?.value || "all";
  let filteredAppointments = appointments;

  if (filter !== "all") {
    filteredAppointments = appointments.filter((apt) => apt.status === filter);
  }

  const container = document.getElementById("adminAppointmentsList");
  container.innerHTML = filteredAppointments
    .map((appointment) => {
      const user = users.find((u) => u.id === appointment.userId);
      const service = services.find((s) => s.id === appointment.serviceId);
      return `
                    <div class="appointment-card">
                        <div class="appointment-header">
                            <h4>${
                              user
                                ? user.firstName + " " + user.lastName
                                : "Unknown User"
                            }</h4>
                            <span class="status status-${appointment.status}">${
        appointment.status
      }</span>
                        </div>
                        <div class="appointment-details">
                            <p><strong>Service:</strong> ${
                              service ? service.name : "Unknown Service"
                            }</p>
                            <p><strong>Date:</strong> ${appointment.date}</p>
                            <p><strong>Time:</strong> ${appointment.time}</p>
                            <p><strong>Payment:</strong> ${
                              appointment.paymentMethod
                            }</p>
                            ${
                              appointment.notes
                                ? `<p><strong>Notes:</strong> ${appointment.notes}</p>`
                                : ""
                            }
                        </div>
                        <div class="appointment-actions">
                            ${
                              appointment.status === "pending"
                                ? `
                                <button class="btn btn-sm btn-success" onclick="updateAppointmentStatus(${appointment.id}, 'confirmed')">Confirm</button>
                                <button class="btn btn-sm btn-danger" onclick="updateAppointmentStatus(${appointment.id}, 'cancelled')">Cancel</button>
                            `
                                : ""
                            }
                            ${
                              appointment.status === "confirmed"
                                ? `
                                <button class="btn btn-sm btn-primary" onclick="updateAppointmentStatus(${appointment.id}, 'completed')">Mark Complete</button>
                            `
                                : ""
                            }
                        </div>
                    </div>
                `;
    })
    .join("");
}

function loadAdminFeedback() {
  const container = document.getElementById("adminFeedbackList");
  container.innerHTML = feedbacks
    .map((feedback) => {
      const user = users.find((u) => u.id === feedback.userId);
      return `
                    <div class="feedback-card">
                        <div class="feedback-header">
                            <h4>${
                              user
                                ? user.firstName + " " + user.lastName
                                : "Anonymous"
                            }</h4>
                            <div class="rating">
                                ${"★".repeat(feedback.rating)}${"☆".repeat(
        5 - feedback.rating
      )}
                            </div>
                        </div>
                        <p class="feedback-text">${feedback.text}</p>
                        <span class="feedback-date">${feedback.date}</span>
                    </div>
                `;
    })
    .join("");
}

function loadAdminProfile() {
  if (currentUser && currentUser.type === "admin") {
    document.getElementById("adminFirstName").value = currentUser.firstName;
    document.getElementById("adminLastName").value = currentUser.lastName;
    document.getElementById("adminEmail").value = currentUser.email;
    document.getElementById("adminPhone").value = currentUser.phone;
    document.getElementById("adminAddress").value = currentUser.address;
  }
}

// User Dashboard Functions
function showUserSection(section) {
  // Hide all sections
  document
    .querySelectorAll("#userDashboard .dashboard-section")
    .forEach((s) => (s.style.display = "none"));

  // Remove active class from all menu items
  document
    .querySelectorAll("#userDashboard .sidebar-menu a")
    .forEach((a) => a.classList.remove("active"));

  // Show selected section
  document.getElementById(
    "user" + section.charAt(0).toUpperCase() + section.slice(1) + "Section"
  ).style.display = "block";

  // Add active class to selected menu item
  event.target.classList.add("active");
}

function loadUserData() {
  loadUserServices();
  loadUserAppointments();
  loadUserProfile();
  loadBookingServices();
}

function loadUserServices() {
  const container = document.getElementById("userServicesList");
  container.innerHTML = services
    .map(
      (service) => `
                <div class="service-card">
                    <h3>${service.name}</h3>
                    <p class="service-description">${service.description}</p>
                    <div class="service-details">
                        <span class="service-price">${service.price}</span>
                        <span class="service-duration">${service.duration} min</span>
                    </div>
                </div>
            `
    )
    .join("");
}

function loadUserAppointments() {
  const userAppointments = appointments.filter(
    (apt) => apt.userId === currentUser.id
  );
  const container = document.getElementById("userAppointmentsList");

  if (userAppointments.length === 0) {
    container.innerHTML = '<p class="no-data">No appointments found.</p>';
    return;
  }

  container.innerHTML = userAppointments
    .map((appointment) => {
      const service = services.find((s) => s.id === appointment.serviceId);
      return `
                    <div class="appointment-card">
                        <div class="appointment-header">
                            <h4>${
                              service ? service.name : "Unknown Service"
                            }</h4>
                            <span class="status status-${appointment.status}">${
        appointment.status
      }</span>
                        </div>
                        <div class="appointment-details">
                            <p><strong>Date:</strong> ${appointment.date}</p>
                            <p><strong>Time:</strong> ${appointment.time}</p>
                            <p><strong>Price:</strong> ${
                              service ? service.price : 0
                            }</p>
                            <p><strong>Payment:</strong> ${
                              appointment.paymentMethod
                            }</p>
                            ${
                              appointment.notes
                                ? `<p><strong>Notes:</strong> ${appointment.notes}</p>`
                                : ""
                            }
                        </div>
                        ${
                          appointment.status === "pending"
                            ? `
                            <div class="appointment-actions">
                                <button class="btn btn-sm btn-danger" onclick="cancelAppointment(${appointment.id})">Cancel</button>
                            </div>
                        `
                            : ""
                        }
                    </div>
                `;
    })
    .join("");
}

function loadUserProfile() {
  if (currentUser && currentUser.type === "user") {
    document.getElementById("userFirstName").value = currentUser.firstName;
    document.getElementById("userLastName").value = currentUser.lastName;
    document.getElementById("userEmail").value = currentUser.email;
    document.getElementById("userPhone").value = currentUser.phone;
    document.getElementById("userAddress").value = currentUser.address;
  }
}

function loadBookingServices() {
  const select = document.getElementById("bookingService");
  select.innerHTML =
    '<option value="">Choose a service</option>' +
    services
      .map(
        (service) =>
          `<option value="${service.id}">${service.name} - ${service.price}</option>`
      )
      .join("");
}

// Service Management
function showAddServiceModal() {
  document.getElementById("addServiceModal").style.display = "block";
}

document
  .getElementById("addServiceForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const newService = {
      id: nextServiceId++,
      name: document.getElementById("serviceName").value,
      description: document.getElementById("serviceDescription").value,
      price: parseFloat(document.getElementById("servicePrice").value),
      duration: parseInt(document.getElementById("serviceDuration").value),
    };

    services.push(newService);
    closeModal("addServiceModal");
    loadAdminServices();
    updateAdminStats();
    showNotification("Service added successfully!", "success");
    document.getElementById("addServiceForm").reset();
  });

function editService(serviceId) {
  const service = services.find((s) => s.id === serviceId);
  if (service) {
    document.getElementById("editServiceId").value = service.id;
    document.getElementById("editServiceName").value = service.name;
    document.getElementById("editServiceDescription").value =
      service.description;
    document.getElementById("editServicePrice").value = service.price;
    document.getElementById("editServiceDuration").value = service.duration;
    document.getElementById("editServiceModal").style.display = "block";
  }
}

document
  .getElementById("editServiceForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const serviceId = parseInt(document.getElementById("editServiceId").value);
    const serviceIndex = services.findIndex((s) => s.id === serviceId);

    if (serviceIndex !== -1) {
      services[serviceIndex] = {
        id: serviceId,
        name: document.getElementById("editServiceName").value,
        description: document.getElementById("editServiceDescription").value,
        price: parseFloat(document.getElementById("editServicePrice").value),
        duration: parseInt(
          document.getElementById("editServiceDuration").value
        ),
      };

      closeModal("editServiceModal");
      loadAdminServices();
      showNotification("Service updated successfully!", "success");
    }
  });

function deleteService(serviceId) {
  if (confirm("Are you sure you want to delete this service?")) {
    services = services.filter((s) => s.id !== serviceId);
    loadAdminServices();
    updateAdminStats();
    showNotification("Service deleted successfully!", "success");
  }
}

// Appointment Management
document.getElementById("bookingForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const serviceId = parseInt(document.getElementById("bookingService").value);
  const date = document.getElementById("bookingDate").value;
  const time = document.getElementById("bookingTime").value;
  const paymentMethod = document.getElementById("paymentMethod").value;
  const notes = document.getElementById("bookingNotes").value;

  const newAppointment = {
    id: nextAppointmentId++,
    userId: currentUser.id,
    serviceId: serviceId,
    date: date,
    time: time,
    paymentMethod: paymentMethod,
    notes: notes,
    status: "pending",
  };

  if (paymentMethod === "online") {
    // Show payment modal
    const service = services.find((s) => s.id === serviceId);
    showPaymentModal(newAppointment, service);
  } else {
    appointments.push(newAppointment);
    showNotification("Appointment booked successfully!", "success");
    document.getElementById("bookingForm").reset();
    loadUserAppointments();
  }
});

function showPaymentModal(appointment, service) {
  const summary = `
                <p><strong>Service:</strong> ${service.name}</p>
                <p><strong>Date:</strong> ${appointment.date}</p>
                <p><strong>Time:</strong> ${appointment.time}</p>
                <p><strong>Duration:</strong> ${service.duration} minutes</p>
                <p><strong>Amount:</strong> ${service.price}</p>
            `;
  document.getElementById("paymentSummary").innerHTML = summary;
  document.getElementById("paymentModal").style.display = "block";

  // Store appointment data for processing after payment
  document
    .getElementById("paymentModal")
    .setAttribute("data-appointment", JSON.stringify(appointment));
}

document.getElementById("paymentForm").addEventListener("submit", function (e) {
  e.preventDefault();

  // Simulate payment processing
  setTimeout(() => {
    const appointmentData = JSON.parse(
      document.getElementById("paymentModal").getAttribute("data-appointment")
    );
    appointments.push(appointmentData);

    closeModal("paymentModal");
    showNotification("Payment successful! Appointment booked.", "success");
    document.getElementById("bookingForm").reset();
    document.getElementById("paymentForm").reset();
    loadUserAppointments();
  }, 2000);

  showNotification("Processing payment...", "info");
});

function updateAppointmentStatus(appointmentId, status) {
  const appointment = appointments.find((apt) => apt.id === appointmentId);
  if (appointment) {
    appointment.status = status;
    loadAdminAppointments();
    updateAdminStats();
    showNotification(`Appointment ${status} successfully!`, "success");
  }
}

function cancelAppointment(appointmentId) {
  if (confirm("Are you sure you want to cancel this appointment?")) {
    updateAppointmentStatus(appointmentId, "cancelled");
    loadUserAppointments();
  }
}

// Feedback Management
document
  .getElementById("feedbackForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const rating = parseInt(
      document.querySelector('input[name="rating"]:checked')?.value || 0
    );
    const text = document.getElementById("feedbackText").value;

    if (rating === 0) {
      showNotification("Please select a rating!", "error");
      return;
    }

    const newFeedback = {
      id: feedbacks.length + 1,
      userId: currentUser.id,
      rating: rating,
      text: text,
      date: new Date().toLocaleDateString(),
    };

    feedbacks.push(newFeedback);
    showNotification("Feedback submitted successfully!", "success");
    document.getElementById("feedbackForm").reset();
  });

// Profile Management
document
  .getElementById("adminProfileForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    currentUser.firstName = document.getElementById("adminFirstName").value;
    currentUser.lastName = document.getElementById("adminLastName").value;
    currentUser.email = document.getElementById("adminEmail").value;
    currentUser.phone = document.getElementById("adminPhone").value;
    currentUser.address = document.getElementById("adminAddress").value;

    // Update user in users array
    const userIndex = users.findIndex((u) => u.id === currentUser.id);
    if (userIndex !== -1) {
      users[userIndex] = currentUser;
    }

    showNotification("Profile updated successfully!", "success");
  });

document
  .getElementById("userProfileForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    currentUser.firstName = document.getElementById("userFirstName").value;
    currentUser.lastName = document.getElementById("userLastName").value;
    currentUser.email = document.getElementById("userEmail").value;
    currentUser.phone = document.getElementById("userPhone").value;
    currentUser.address = document.getElementById("userAddress").value;

    // Update user in users array
    const userIndex = users.findIndex((u) => u.id === currentUser.id);
    if (userIndex !== -1) {
      users[userIndex] = currentUser;
    }

    showNotification("Profile updated successfully!", "success");
  });

// Schedule Management
document
  .getElementById("scheduleForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    showNotification("Schedule updated successfully!", "success");
  });

// Appointment filter
document
  .getElementById("appointmentFilter")
  ?.addEventListener("change", function () {
    loadAdminAppointments();
  });

// Public services loading
function loadPublicServices() {
  const container = document.getElementById("publicServicesList");
  container.innerHTML = services
    .map(
      (service) => `
                <div class="service-card">
                    <h3>${service.name}</h3>
                    <p class="service-description">${service.description}</p>
                    <div class="service-details">
                        <span class="service-price">${service.price}</span>
                        <span class="service-duration">${service.duration} min</span>
                    </div>
                </div>
            `
    )
    .join("");
}

// Utility functions
function showNotification(message, type) {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
                <span>${message}</span>
                <button onclick="this.parentElement.remove()">&times;</button>
            `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.remove();
  }, 5000);
}

function scrollToSection(sectionId) {
  document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
}

// Input formatting
document.getElementById("cardNumber")?.addEventListener("input", function (e) {
  let value = e.target.value.replace(/\s/g, "").replace(/[^0-9]/gi, "");
  let formattedValue = value.match(/.{1,4}/g)?.join(" ") || value;
  e.target.value = formattedValue;
});

document.getElementById("expiryDate")?.addEventListener("input", function (e) {
  let value = e.target.value.replace(/\D/g, "");
  if (value.length >= 2) {
    value = value.substring(0, 2) + "/" + value.substring(2, 4);
  }
  e.target.value = value;
});

document.getElementById("cvv")?.addEventListener("input", function (e) {
  e.target.value = e.target.value.replace(/[^0-9]/g, "");
});

// Signup form handling
document
  .getElementById("signupUserType")
  .addEventListener("change", function () {
    const addressLabel = document.getElementById("addressLabel");
    if (this.value === "admin") {
      addressLabel.textContent = "Salon Address";
    } else {
      addressLabel.textContent = "Address";
    }
  });

// Initialize
document.addEventListener("DOMContentLoaded", function () {
  loadPublicServices();

  // Set minimum date for booking
  const today = new Date().toISOString().split("T")[0];
  document.getElementById("bookingDate").min = today;
});

// Close modal when clicking outside
window.addEventListener("click", function (e) {
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

// ####################################################################################################################


