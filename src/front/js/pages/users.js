import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Users = () => {
	const { store, actions } = useContext(Context);

    useEffect(()=> {
        actions.getUsers()
    }, []);

    console.log(store);

    const{users} = store;

    if (!users.length){
        return null
    }

	return (
		<div className="text-center mt-5">
			<ul>
                {user.map((user) =>
                <li key={user.id}>
                    <p> {user.email}</p>
                </li>
            )}
            </ul>
		</div>
	);
};
