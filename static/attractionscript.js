let pathVariable = window.location.pathname.split('/')[2];

let url = "http://18.139.199.228:3000/api/attractions/"+pathVariable



fetch(url).then((taipei)=>{
    return taipei.json();
})
.then((data)=>{
        let len=data.data.image.length;
        for (n=0 ; n < len ; n++){
            let title = data.data.name
            let subtitle = data.data.category+" at "+data.data.mrt
            let description=data.data.description
            let address=data.data.address
            let transport=data.data.transport
            let image=data.data.image[n]
            document.querySelector(".title").textContent=title
            document.querySelector(".mrt").textContent=subtitle
            document.querySelector(".description .intro").textContent=description
            document.querySelector(".description .address").textContent=address
            document.querySelector(".description .transhow").textContent=transport
            let carousel = document.querySelector(".imageCarousel")
            let btn = document.querySelector(".left")
            let images = document.createElement('img');
            images.src=image
            carousel.insertBefore(images,btn);
            let dots = document.querySelector(".dots")
            let dot = document.createElement('span')
            dot.classList.add("dot"+n)
            dots.append(dot)

        }
        let image0 = document.getElementsByTagName('img').item(0);
        image0.style.display='block'
        let dot0 =document.querySelectorAll('span[class^="dot"]').item(0)
        dot0.style.background="black"
})

// 輪播圖片
let index = 1
function slides(n){
    let slideindex = index+n;
    let length=document.getElementsByTagName('img').length;
    let array=document.getElementsByTagName('img');
    let dots=document.querySelectorAll('span[class^="dot"]')
    if (slideindex>length){
        slideindex=1;
        index=0
    }
    if (slideindex<=0){
        index=length+1
        slideindex=length
    }
    for(i=0;i<length;i++){
        array[i].style.display='none';
        dots[i].style.background="white"
    }
    array[slideindex-1].style.display='block';
    dots[slideindex-1].style.background="black"
    console.log(slideindex);
    index=index+n ;
}


// 選擇時段
document.getElementsByName('tourtime').forEach(radio=>{
    radio.addEventListener('click',function(){
        if(radio.value=="morning"){
            document.querySelector(".price").textContent=2000
        }
        if(radio.value=="afternoon"){
            document.querySelector(".price").textContent=2500
        }
    })
})

