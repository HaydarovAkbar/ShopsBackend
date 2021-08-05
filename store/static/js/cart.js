var updateBtns = document.getElementsByClassName('update-details')
console.log(updateBtns)

log_element = document.getElementById('login')
if (user == 'AnonymousUser'){
    log_element.innerHTML = 'Log in'
}
else{
    log_element.innerHTML = 'Salom, ' + user
}

for( i = 0; i< updateBtns.length; i++ ){
    updateBtns[i].addEventListener('click',function(){
       product_id = this.dataset.product
       action = this.dataset.action
       console.log(product_id,action)
       if (user == 'AnonymousUser'){
            console.log("ro'yxatdan o'tmagan!")
       }
       else{
           update_order_details(product_id,action)
       }
    })
}
function update_order_details(product_id,action){
    console.log("ro'yxatdan o'tgan, ma'lumotlar jo'natildi")
    url = '/store/update_details/'
    fetch(url,{
    method:'POST',
    headers:{
        'Content-Type':'application/json',
        'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'product_id':product_id,'action':action})
    })
    .then((response)=>{
    console.log(response.json())
    })
    .then((data)=>{
    location.reload()
    })
    console.log("Ma'lumot yetkazildi!")
}