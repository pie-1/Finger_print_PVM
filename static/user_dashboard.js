document.addEventListener("DOMContentLoaded", () => {
  const addUserBtn = document.getElementById("addUserBtn");
  const userModal = document.getElementById("userModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const userForm = document.getElementById("userForm");
  const formTitle = document.getElementById("formTitle");
  const userTableBody = document.getElementById("userTableBody");
  
  /*let users = [
    { id: "1", name: "John Doe", clg: "Kathmandu College" },
    { id: "2", name: "Jane Smith", clg: "Pokhara University" },
  ];*/
  let users=document.user || [];
  let editIndex = -1; 

  const openModal = (action, user = null, index = -1) => {
    formTitle.textContent = `${action} User`;
    userForm.dataset.action = action;
    if (action === "Edit") {
      userForm.id.value = user.id;
      userForm.name.value = user.name;      
      userForm.sem.value = user.sem;
      userForm.dep.value = user.dep;   
      editIndex = index;
    } else {
      userForm.reset();
    }
    userModal.style.display = "flex";
  };

  const closeModal = () => {
    userModal.style.display = "none";
  };  

  const renderTable = ( ) => {
    
    userTableBody.innerHTML = users
      .map(
        (user, index) => `
          <tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.sem}</td>
            <td>${user.dep}</td>
            <td>${user.fingerprintFile || "N/A"}</td>
              <td>
            <button onclick="editUser(${index})">Edit</button>
            <button onclick="deleteUser(${index})" style="background-color: #dc3545;">Delete</button>
              </td>
          </tr>`
      )
      .join(""); 
  };
  

  const editUser = (index) => {
    const user = users[index];
    openModal("Edit", user, index);
  };

  const deleteUser = (index) => {
    users.splice(index, 1);
    renderTable();
  };  

  userForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(userForm);
    const user = Object.fromEntries(formData.entries());
    const action = userForm.dataset.action;

    if (action === "Add") {
      users.push(user);
    } else if (action === "Edit") {
      users[editIndex] = user;
    }

    renderTable();
    closeModal();
  });

  addUserBtn.addEventListener("click", () => openModal("Add"));
  closeModalBtn.addEventListener("click", closeModal);
  window.editUser = editUser; 
  window.deleteUser = deleteUser; 

  window.addEventListener("click", (e) => {
    if (e.target === userModal) closeModal();
  });
  renderTable();
});
