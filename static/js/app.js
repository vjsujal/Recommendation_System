class Chatbox {
  constructor() {
    this.args = {
      chatSection : document.querySelector(".chatbox"),
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
      imageUploadInput: document.getElementById("image-upload"),
      enterMessageInput: document.querySelector(".enter_msge"),
    };

    this.uploadedImage = null;
    this.state = false;
    this.messages = [
      { type: "text1", name: "Sam", message: "Hello, I am AI, Can I recommend some products for you ?" }
    ]; 
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendMessage(chatBox));

    const node = chatBox.querySelector("input[type=text]");

    node.addEventListener("keyup", (key) => {
      if (key.keyCode === 13) {
        this.onSendMessage(chatBox);
      }
    });
  }

  toggleState(chatBox) {
    this.state = !this.state;

    if (this.state) {
      // change the z-index of chatSection
      this.args.chatSection.style.zIndex = 1000;
      chatBox.classList.add("chatbox--active");
    } else {
      // change the z-index of chatSection
      this.args.chatSection.style.zIndex = -123456;
      chatBox.classList.remove("chatbox--active");
    }
  }


  onSendMessage(chatBox) {
    var textField = chatBox.querySelector("input[type=text]");
    var imgField = chatBox.querySelector("input[type=file]");
    var text1 = textField.value;
    var img1 = imgField.files[0]; // Use files array to get the uploaded image

    if (text1 === "" && !img1) {
      return;
    }

    // If image is uploaded, handle image upload
    if (img1 && text1 == "") {
      this.handleImageUpload(chatBox, img1);
    } else if (!img1 && text1 !== "") {
      // Otherwise, continue with text message
      this.handleTextMessage(chatBox, text1);
    }else {
      // Otherwise, continue with text message
      this.handleBoth(chatBox, text1, img1);
    } 
    

    // Clear input fields
    textField.value = "";
    imgField.value = "";
  }

  handleTextMessage(chatBox, text) {
    let userMsg = { type: "text", name: "User", message: text };
    this.messages.push(userMsg);
    this.messages.push({ type: "text1", name: "Sam", message: "Finding results for you..." });

    this.updateChatText(chatBox);

    fetch($SCRIPT_ROOT + "/submit_txt", {
      method: "POST",
      body: JSON.stringify({ message: text }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        if ("answer" in r) {
            let aiMsg = { type: "text1", name: "Sam", message: r.answer };
            this.messages.pop();
            this.messages.push(aiMsg);
        } else {
          let aiMsg = { 
            type: "card", 
            name: "Sam", 
            item1Id:r.item1[0], item1Name:r.item1[1], item1Url:r.item1[2], item1Price:r.item1[3], item1OGPrice:r.item1[4], item1Discount:r.item1[5],
            item2Id:r.item2[0], item2Name:r.item2[1], item2Url:r.item2[2], item2Price:r.item2[3], item2OGPrice:r.item2[4], item2Discount:r.item2[5],
            item3Id:r.item3[0], item3Name:r.item3[1], item3Url:r.item3[2], item3Price:r.item3[3], item3OGPrice:r.item3[4], item3Discount:r.item3[5],
            item4Id:r.item4[0], item4Name:r.item4[1], item4Url:r.item4[2], item4Price:r.item4[3], item4OGPrice:r.item4[4], item4Discount:r.item4[5],
            item5Id:r.item5[0], item5Name:r.item5[1], item5Url:r.item5[2], item5Price:r.item5[3], item5OGPrice:r.item5[4], item5Discount:r.item5[5]
          };
          this.messages.pop();
          this.messages.push(aiMsg);
        }
        this.updateChatText(chatBox);
        })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatBox);
      });
  }

  handleImageUpload(chatBox, img) {
    // Perform any necessary operations related to image upload
    // For now, let's assume the image upload is successful and proceed with updating the chat

    // Convert the image data to a FormData object
    let formData = new FormData();
    formData.append('image', img);

    // Update the chat with the user's message
    let userMsg = { type: "image", name: "User", image: img };
    this.messages.push(userMsg);
    this.messages.push({ type: "text1", name: "Sam", message: "Typing...." });

    this.updateChatText(chatBox);

    // Send the image data in binary format
    fetch($SCRIPT_ROOT + "/submit_img", {
        method: "POST",
        body: formData,  // Use the FormData object as the body
        mode: "cors",
    })
    .then((r) => r.json())
      .then((r) => {
        let aiMsg = { 
          type: "card", 
          name: "Sam", 
          item1Id:r.item1[0], item1Name:r.item1[1], item1Url:r.item1[2], item1Price:r.item1[3], item1OGPrice:r.item1[4], item1Discount:r.item1[5],
          item2Id:r.item2[0], item2Name:r.item2[1], item2Url:r.item2[2], item2Price:r.item2[3], item2OGPrice:r.item2[4], item2Discount:r.item2[5],
          item3Id:r.item3[0], item3Name:r.item3[1], item3Url:r.item3[2], item3Price:r.item3[3], item3OGPrice:r.item3[4], item3Discount:r.item3[5],
          item4Id:r.item4[0], item4Name:r.item4[1], item4Url:r.item4[2], item4Price:r.item4[3], item4OGPrice:r.item4[4], item4Discount:r.item4[5],
          item5Id:r.item5[0], item5Name:r.item5[1], item5Url:r.item5[2], item5Price:r.item5[3], item5OGPrice:r.item5[4], item5Discount:r.item5[5]
        };
        this.messages.pop();
        this.messages.push(aiMsg);
        this.updateChatText(chatBox);
        })
    .catch(error => {
        console.error("Error:", error);
        this.updateChatText(chatBox);
    });
}

    

  handleBoth(chatBox, text, img) {
    // Convert the image data to a FormData object
    let formData1 = new FormData();
    formData1.append('image', img);
    formData1.append('message', text);
    let userMsg = { type: "both", name: "User", message: text, image: img };
    this.messages.push(userMsg);
    this.messages.push({ type: "text1", name: "Sam", message: "Typing...." });
    this.updateChatText(chatBox);
    fetch($SCRIPT_ROOT + "/submit_both", {
      method: "POST",
      body: formData1,  // Use the FormData object as the body
      mode: "cors",
  })
  .then((r) => r.json())
    .then((r) => {
      let aiMsg = { 
        type: "card", 
        name: "Sam", 
        item1Id:r.item1[0], item1Name:r.item1[1], item1Url:r.item1[2], item1Price:r.item1[3], item1OGPrice:r.item1[4], item1Discount:r.item1[5],
        item2Id:r.item2[0], item2Name:r.item2[1], item2Url:r.item2[2], item2Price:r.item2[3], item2OGPrice:r.item2[4], item2Discount:r.item2[5],
        item3Id:r.item3[0], item3Name:r.item3[1], item3Url:r.item3[2], item3Price:r.item3[3], item3OGPrice:r.item3[4], item3Discount:r.item3[5],
        item4Id:r.item4[0], item4Name:r.item4[1], item4Url:r.item4[2], item4Price:r.item4[3], item4OGPrice:r.item4[4], item4Discount:r.item4[5],
        item5Id:r.item5[0], item5Name:r.item5[1], item5Url:r.item5[2], item5Price:r.item5[3], item5OGPrice:r.item5[4], item5Discount:r.item5[5]
      };
      this.messages.pop();
      this.messages.push(aiMsg);
      this.updateChatText(chatBox);
      })
  .catch(error => {
      console.error("Error:", error);
      this.updateChatText(chatBox);
  });
  }

  updateChatText(chatBox) {
    var html = '';
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name === "Sam") {
          if (item.type === "card") {
            html +=
              `<div style="display: flex; align-items: center; gap: 0.5rem; margin: 10px 0;">
              <i class="fas fa-user" style="width: 20px; height: 20px; border-radius: 50%;" alt="image"></i>
              <div style="border-radius: 12px; width: 100%; padding: 1.5rem; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%);">
                <ul style="display: flex; padding: 0rem 0rem; list-style: none; overflow-x: scroll; scroll-snap-type: x mandatory;">
                <li style="flex: 1 0 70%; padding: 20px; background: #2A2F33; border-radius: 12px; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%); scroll-snap-align: start; transition: all 0.2s; margin-right: 10px; align-items: center;">                  
                <div style="align-items: center; text-align: center;" >
                    <img style="height: 180px; align-items:center; margin:8px" src="${item.item1Url}" alt="">
                    <div style="margin: 20px 0; text-align: left; color: white;">
                    <p title="${item.item1Name}" style="display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; font-size: 15px;" >${item.item1Name}</p>
                    <p style="color:red; font-size: 12px;" >${item.item1Discount}% OFF</p>
                      <p style="font-size: 15px;" >₹${item.item1Price}.00 <del style="font-size: 12px; color:red">₹${item.item1OGPrice}.00</del></p>
                    </div>
                  </div>
                  <div style="margin-top: auto;">
                    <a id="viewButton1" href="view_item/${item.item1Id}" style="font-size:17px; display: inline-block; text-decoration: none; color: white; background: #ef233c; padding: 3px 25px; border-radius: 8px; transition: background 0.2s;">View</a>
                  </div>
                </li>
                <li style="flex: 1 0 70%; padding: 20px; background: #2A2F33; border-radius: 12px; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%); scroll-snap-align: start; transition: all 0.2s; margin-right: 10px; align-items: center;">                  <div style="align-items: center; text-align: center;" >
                    <img style="height: 180px; margin:8px" src="${item.item2Url}" alt="">
                    <div style="margin: 20px 0; text-align: left; color: white;">
                    <p title="${item.item2Name}" style="display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; font-size: 15px;" >${item.item2Name}</p>
                    <p style="color:red; font-size: 12px;" >${item.item2Discount}% OFF</p>
                      <p style="font-size: 15px;" >₹${item.item2Price}.00 <del style="font-size: 12px; color:red">₹${item.item2OGPrice}.00</del></p>
                    </div>
                  </div>
                  <div style="margin-top: auto;">
                  <a id="viewButton2" href="view_item/${item.item2Id}" style="font-size:17px; display: inline-block; text-decoration: none; color: white; background: #ef233c; padding: 3px 25px; border-radius: 8px; transition: background 0.2s;">View</a>
                  </div>
                </li>
                <li style="flex: 1 0 70%; padding: 20px; background: #2A2F33; border-radius: 12px; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%); scroll-snap-align: start; transition: all 0.2s; margin-right: 10px; align-items: center;">                  <div style="align-items: center; text-align: center;" >
                    <img style="height: 180px; margin:8px" src="${item.item3Url}" alt="">
                    <div style="margin: 20px 0; text-align: left; color: white;">
                    <p title="${item.item3Name}" style="display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; font-size: 15px;" >${item.item3Name}</p>
                    <p style="color:red; font-size: 12px;" >${item.item3Discount}% OFF</p>
                      <p style="font-size: 15px;" >₹${item.item3Price}.00 <del style="font-size: 12px; color:red">₹${item.item3OGPrice}.00</del></p>
                    </div>
                  </div>
                  <div style="margin-top: auto;">
                  <a id="viewButton3" href="view_item/${item.item3Id}" style="font-size:17px; display: inline-block; text-decoration: none; color: white; background: #ef233c; padding: 3px 25px; border-radius: 8px; transition: background 0.2s;">View</a>
                  </div>
                </li>
                <li style="flex: 1 0 70%; padding: 20px; background: #2A2F33; border-radius: 12px; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%); scroll-snap-align: start; transition: all 0.2s; margin-right: 10px; align-items: center;">                  <div style="align-items: center; text-align: center;" >
                    <img style="height: 180px; margin:8px" src="${item.item4Url}" alt="">
                    <div style="margin: 20px 0; text-align: left; color: white;">
                    <p title="${item.item4Name}" style="display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; font-size: 15px;" >${item.item4Name}</p>
                    <p style="color:red; font-size: 12px;" >${item.item4Discount}% OFF</p>
                      <p style="font-size: 15px;" >₹${item.item4Price}.00 <del style="font-size: 12px; color:red">₹${item.item4OGPrice}.00</del></p>
                    </div>
                  </div>
                  <div style="margin-top: auto;">
                  <a id="viewButton4" href="view_item/${item.item4Id}" style="font-size:17px; display: inline-block; text-decoration: none; color: white; background: #ef233c; padding: 3px 25px; border-radius: 8px; transition: background 0.2s;">View</a>
                  </div>
                </li>
                <li style="flex: 1 0 70%; padding: 20px; background: #2A2F33; border-radius: 12px; box-shadow: 0 5px 15px rgba(0, 0, 0, 15%); scroll-snap-align: start; transition: all 0.2s; margin-right: 10px; align-items: center;">                  <div style="align-items: center; text-align: center;" >
                    <img style="height: 180px; margin:8px" src="${item.item5Url}" alt="">
                    <div style="margin: 20px 0; text-align: left; color: white;">
                      <p title="${item.item5Name}" style="display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 3; font-size: 15px;" >${item.item5Name}</p>
                      <p style="color:red; font-size: 12px;" >${item.item5Discount}% OFF</p>
                      <p style="font-size: 15px;" >₹${item.item5Price}.00 <del style="font-size: 12px; color:red">₹${item.item5OGPrice}.00</del></p>
                    </div>
                  </div>
                  <div style="margin-top: auto;">
                  <a id="viewButton5" href="view_item/${item.item5Id}" style="font-size:17px; display: inline-block; text-decoration: none; color: white; background: #ef233c; padding: 3px 25px; border-radius: 8px; transition: background 0.2s;">View</a>
                  </div>
                </li>
                
              </ul>
            </div>
            </div>`;
          }else{
            html +=
            '<div style="display: flex; align-items: end; gap:0.5rem; margin: 10px 0 "><i class="fas fa-user" style="width: 20px; height: 20px; border-radius: 50%;" alt="image"></i><div class="messages__item messages__item--visitor">'
            +item.message+
            '</div></div>';
          }
        } else {
          if (item.type === "text") {
            html +=
              '<div class="messages__item messages__item--operator">' +
              item.message +
              "</div>";
          } else if (item.type === "image") {
            html +=
            '<div class="messages__item messages__item--operator"><img src="' +
            URL.createObjectURL(item.image) +
            '" style="max-width: 100%; max-height: 200px; margin-top: 10px;"/></div>';
          } else if (item.type === "both") {
            html +=
              '<div style="padding-left:12px" class="messages__item messages__item--operator">' +
              '<img src="' +
              URL.createObjectURL(item.image) +
              '" style="max-width: 100%; max-height: 200px; margin-top: 10px;"/><br><br>'+item.message+'</div>';
          }
        }
      });
  
    const chatMessage = chatBox.querySelector(".chatbox__messages");
    chatMessage.innerHTML = html;
    chatMessage.scrollTop = chatMessage.scrollHeight;
  }
}

const chatbox = new Chatbox();
chatbox.display();
chatbox.updateChatText(document.querySelector(".chatbox__support"));