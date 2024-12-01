import React from "react";
import Instance from "../../api/instance";
export default function Contractor() {
  function getMyOrders(){
    Instance.get()
  }
  return (
    <div
      className="contractor-wrapper centered-into-wrappers text-color"
      style={{ "--font-size": "10em" }}
    >
      {localStorage.getItem("wallet_balance")}
    </div>
  );
}
