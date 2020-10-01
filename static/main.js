//Get modal element
var modal = document.getElementById('modal');
//Get open modal button
var modalBtn = document.querySelectorAll('.open-modal');
//Get close button
var closeBtn = document.getElementById('cancel-button');
//Get delete button
var deleteBtn = document.getElementById('delete-button');
//Get redirection link for the delete function
var redirect;

//Listen for open click
for (let i=0; i<modalBtn.length; i++){
    redirect = modalBtn[i].href
    modalBtn[i].addEventListener('click', openModal);
}
//Listen for close click
closeBtn.addEventListener('click', closeModal);
//Listen for outside click
window.addEventListener('click', outsideClick)
//Listen for delete click
deleteBtn.addEventListener('click', deleteRow)

function openModal(e){
    modal.style.display = 'block';
    e.preventDefault();
}

function deleteRow(){
    window.location = redirect;
}

function closeModal(){
    modal.style.display = 'none';
}

function outsideClick(e){
    if (e.target == modal){
        modal.style.display = 'none';
    }
}