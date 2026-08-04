<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.12.2" name="traps" tilewidth="54" tileheight="52" tilecount="12" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="block">
  <image source="../../assets/Traps/block.png" width="22" height="22"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="3" y="3" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="1" type="brown_platform">
  <image source="../../assets/Traps/brown_platform.png" width="32" height="8"/>
  <animation>
   <frame tileid="10" duration="100"/>
   <frame tileid="2" duration="100"/>
  </animation>
 </tile>
 <tile id="2" type="falling_platform">
  <image source="../../assets/Traps/falling_platform.png" width="32" height="10"/>
 </tile>
 <tile id="3" type="fan">
  <image source="../../assets/Traps/fan.png" width="24" height="8"/>
 </tile>
 <tile id="4" type="fire">
  <image source="../../assets/Traps/fire.png" width="16" height="32"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="16" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="5" type="grey_platform">
  <image source="../../assets/Traps/grey_platform.png" width="32" height="8"/>
 </tile>
 <tile id="6" type="rock_head">
  <image source="../../assets/Traps/rock_head.png" width="42" height="42"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="5" y="5" width="32" height="32"/>
  </objectgroup>
 </tile>
 <tile id="7" type="saw">
  <image source="../../assets/Traps/saw.png" width="38" height="38"/>
 </tile>
 <tile id="8" type="spike">
  <image source="../../assets/Traps/spike.png" width="16" height="16"/>
  <objectgroup draworder="index" id="2">
   <object id="6" x="0" y="9" width="16" height="7"/>
  </objectgroup>
 </tile>
 <tile id="9" type="spike_head">
  <image source="../../assets/Traps/spike_head.png" width="54" height="52"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="9" y="8.09091" width="37" height="37"/>
  </objectgroup>
 </tile>
 <tile id="10" type="spiked_ball">
  <image source="../../assets/Traps/spiked_ball.png" width="28" height="28"/>
 </tile>
 <tile id="11" type="trampoline">
  <image source="../../assets/Traps/trampoline.png" width="28" height="28"/>
  <objectgroup draworder="index" id="2">
   <object id="1" x="2" y="17" width="23" height="11"/>
  </objectgroup>
 </tile>
</tileset>
