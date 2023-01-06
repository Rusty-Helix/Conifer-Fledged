const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

let previousAvatar = null;

if (document.querySelector(".update-account")){
  const inputList = document.querySelectorAll("input");
  const labelList = document.querySelectorAll("label");
  // const linkList = document.querySelectorAll("a")
  const avatarFileInput = document.querySelector("#id_avatar")
// console.log(avatarFileInput)
  avatarFileInput.addEventListener("change", handleFiles, false);
  function handleFiles() {
    
    

    const firstFormGroup = document.querySelectorAll(".form__group")[0]
    const uploadedAvatar = document.createElement("img");
    const reader = new FileReader()

    reader.addEventListener("load", ()=>{
      uploadedAvatar.src = reader.result
    })

    reader.readAsDataURL(this.files[0])

    uploadedAvatar.classList.add("avatar-preview")
    
    const h2Separator = document.createElement("h2");
    h2Separator.textContent = "Uploaded Avatar:"
    
    if (previousAvatar !== null){
      previousAvatar.remove()
      previousH2.remove()
    }

    firstFormGroup.appendChild(h2Separator)
    firstFormGroup.appendChild(uploadedAvatar)

    previousAvatar = uploadedAvatar
    previousH2 = h2Separator
  }

  // const imageSrcString = linkList[7].href
  // const shortImageSrcString = imageSrcString.substring(imageSrcString.lastIndexOf('/')+1)


  // const currentAvatar = document.createElement("img");
  // currentAvatar.src = imageSrcString;
  // currentAvatar.classList.add("avatar-preview")
  
  

  inputList[2].remove();
  labelList[1].remove();
  labelList[2].remove();
  


}


// inputList.forEach(function (input, index) {
//   console.log(input, index);
//   if (input.htmlFor == 'profile_pic') {
//     input.remove();
//     console.log(input)
//   }
//   if (input.htmlFor == 'avatar_clear_id') {
//     input.remove();
//     console.log(input)
//   }
// });


// firstInput.remove()
// firstLabel.remove()

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

