import axios from "axios";

const BASE_URL = "https://huuquangn2005.pythonanywhere.com";

export const endpoints = {
    'categories': '/apis/categories/',
    'foods': '/apis/foods/',
    'orders': '/apis/orders/',
    'register': '/apis/accounts/',
    'login': '/o/token/',
    "current-user": "/apis/accounts/me/",
    'ingredients': "/apis/ingredients/",
    'reservations': "/apis/reservations/",
};

export const authApis = (token) => {
    return axios.create({
        baseURL: BASE_URL,
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
}


export default axios.create({
    baseURL: BASE_URL
});