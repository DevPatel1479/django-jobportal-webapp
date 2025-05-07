document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.role-tab');
    const jobProviderFields = document.querySelector('.jobprovider-only');
    const selectedRoleInput = document.getElementById('selectedRole');
    const uploadBtn = document.getElementById('uploadBtn');
    const documentInput = document.getElementById('documentUpload');
    const filePreview = document.querySelector('.file-preview');
    const fileName = document.querySelector('.file-name');
    const btnChange = document.querySelector('.btn-change');
    const btnRemove = document.querySelector('.btn-remove');
    let currentRole = selectedRoleInput ? selectedRoleInput.value : 'jobseeker';
    const companyNameInput = document.getElementById('company_name');

    console.log("Initial selected role from input:", currentRole);

    // Set tab UI based on role
    function updateTabUI(role) {
        console.log("Updating UI for role:", role);
        tabs.forEach(tab => tab.classList.remove('active'));
        const activeTab = document.querySelector(`.role-tab[data-role="${role}"]`);
        if (activeTab) activeTab.classList.add('active');

        if (role === 'jobprovider') {
            jobProviderFields.style.display = 'block';
        } else {
            jobProviderFields.style.display = 'none';
        }

        selectedRoleInput.value = role;
        console.log("Hidden input updated to:", selectedRoleInput.value);
    }

    updateTabUI(currentRole);
    // On tab click, update role + hidden input
    tabs.forEach(tab => {
        tab.addEventListener('click', function () {
            const selectedRole = this.getAttribute('data-role');
            console.log("Selected role from click: ", selectedRole);
            updateTabUI(selectedRole);
        });
    });
    if (uploadBtn && documentInput) {
        uploadBtn.addEventListener('click', function (e) {
            e.preventDefault();  // Prevent scroll/jump
            documentInput.click();
        });
    }

    // Handle file selection preview
    if (documentInput) {
        documentInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                filePreview.style.display = 'flex';
                fileName.textContent = this.files[0].name;
            }
        });
    }

    // Change File
    if (btnChange) {
        btnChange.addEventListener('click', function (e) {
            e.preventDefault();
            documentInput.click();
        });
    }

    // Remove File
    if (btnRemove) {
        btnRemove.addEventListener('click', function (e) {
            e.preventDefault();
            documentInput.value = '';
            filePreview.style.display = 'none';
            fileName.textContent = 'No file selected';
        });
    }
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const selectedRole = tab.dataset.role;
            console.log("Selected role from click: ", selectedRole);  
            selectedRoleInput.value = selectedRole;
            
            if (selectedRole === 'jobprovider') {
                
                jobProviderFields.style.display = 'block';
                documentInput.required = true;
                companyNameInput.required = true; 
            } else {
                jobProviderFields.style.display = 'none';
                documentInput.required = false;
                documentInput.value      = '';
                companyNameInput.required = false; 
                
            }
        });
    });

    // // Set initial visibility (in case Job Provider is selected on load)
    // const activeTab = document.querySelector('.role-tab.active');
    // if (activeTab.dataset.role === 'jobprovider') {
    //     jobProviderFields.style.display = 'block';
    // }
    // if (activeTab) {
    //     const role = activeTab.dataset.role;
    //     selectedRoleInput.value = role; // ✅ Set the value on load
    //     if (role === 'jobprovider') {
    //         jobProviderFields.style.display = 'block';
    //     } else {
    //         jobProviderFields.style.display = 'none';
    //     }}
    const activeTab = document.querySelector('.role-tab.active');
    if (activeTab) {
        const role = activeTab.dataset.role;
        selectedRoleInput.value = role;
        if (role === 'jobprovider') {
            jobProviderFields.style.display = 'block';
            documentInput.required = true;
            companyNameInput.required = true; 
        } else {
            jobProviderFields.style.display = 'none';
            documentInput.required = false;
            companyNameInput.required = false; 
        }
    }
});
