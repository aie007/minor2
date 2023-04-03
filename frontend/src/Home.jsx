import React from 'react'
import HeroSection from './Components/HeroSection'
const Home = () => {
  const data = {
    name : "New Inventory shop",
    image : "./Images/docs.png",
  }
  return (
    // <div>Home</div>
    <HeroSection {...data} />

  )
}

export default Home