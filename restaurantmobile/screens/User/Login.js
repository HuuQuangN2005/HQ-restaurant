import { Text, View, Image } from "react-native";
import { TextInput, Button, HelperText } from "react-native-paper";
import LoginStyle from "../../styles/LoginStyle";
import { useContext, useState } from "react";
import { useNavigation } from "@react-navigation/native";
import { OAUTH_CONFIG } from "../../utils/authConfig";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import { MyUserContext } from "../../utils/MyContext";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRoute } from "@react-navigation/native";

const Login = () => {
    const info = [
        { 
            label: "Tên đăng nhập", 
            field: "username", 
            icon: "account" 
        },
        { 
            label: "Mật khẩu", 
            field: "password", 
            icon: "eye", 
            secureTextEntry: true 
        }
    ];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();
    const [,dispatch] = useContext(MyUserContext);
    const route = useRoute();

    const validate = () => {
        if (!user.username || !user.password) {
            setErrMsg("Vui lòng nhập tên đăng nhập và mật khẩu!");
            return false;
        }

        if (user.username.trim().length <= 0) {
            setErrMsg("Tên đăng nhập không hợp lệ!");
            return false;
        }

        setErrMsg(null);
        return true;
    };


    const login = async () => {
        if (validate()) {
            try {
                setLoading(true)
                const data = new URLSearchParams();
                data.append("grant_type", "password");
                data.append("username", user.username);
                data.append("password", user.password);
                data.append("client_id", OAUTH_CONFIG.client_id);
                data.append("client_secret", OAUTH_CONFIG.client_secret);
                let res = await Apis.post(
                    endpoints["login"],
                    data,
                    {
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded",
                        },
                    }
                );

                const token = res.data.access_token;
                await AsyncStorage.setItem("access_token", token);
                let u = await authApis(token).get(endpoints["current-user"]);
                dispatch({
                    type: "login",
                    payload: u.data,
                });

                const next = route.params?.next;
                const params = route.params?.params;
                if (next) {
                    nav.navigate(next, params);
                } else {
                    nav.navigate("Main", {
                        screen: "Profile"
                    });
                }

            } catch (ex) {
                setErrMsg("Đã có lỗi xảy ra. Vui lòng thử lại sau!");
                console.info(ex);
            } finally {
                setLoading(false);
            }
        }
    }

    return (
        <View style={LoginStyle.container}>
            <Text style={LoginStyle.title}>ĐĂNG NHẬP NGƯỜI DÙNG</Text>
            <HelperText type="error" visible={errMsg}>
                {errMsg}
            </HelperText>
            {info.map(i => (
                <TextInput
                    key={i.field}
                    style={[LoginStyle.input, { marginVertical: 6 }]}
                    label={i.label}
                    secureTextEntry={i.secureTextEntry}
                    right={<TextInput.Icon icon={i.icon} />}
                    value={user[i.field]}
                    autoCapitalize="none"
                    onChangeText={t => setUser({ ...user, [i.field]: t })}
                />
            ))}

            {user.avatar && ( <Image source={{ uri: user.avatar.uri }} style={LoginStyle.avatar}/>)}

            <Button mode="contained" loading={loading} disabled={loading} style={LoginStyle.loginBtn} labelStyle={LoginStyle.loginText} onPress={login} >
                 Đăng nhập
            </Button>
            <Text style={LoginStyle.registerText}>
                Chưa có tài khoản?{" "}
                <Text style={LoginStyle.registerLink} onPress={() => nav.navigate('Register')}>
                 Đăng ký
                </Text>
            </Text>
        </View>
    );
}

export default Login;