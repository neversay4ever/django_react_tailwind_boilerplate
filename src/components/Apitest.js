import React, { useState, useEffect } from 'react';
import axios from 'axios'

const Apitest = () => {
    const url = process.env.REACT_APP_API_DOMAIN + '/api/test'

    const [data, setData] = useState([]);

    const fetchData = async () => {
        const result = await axios(url);
        setData(result.data);
    };

    useEffect(() => {

        fetchData();
    }, []);

    return (
        <ul>
            {data.map(item => (
                <li key={item.objectID}>
                    <a href={item.name} className='text-red-500'>{item.email}</a>
                </li>
            ))}
        </ul>
    );
}

export default Apitest;


