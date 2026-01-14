import { Text, TouchableOpacity, View, Alert, Image } from "react-native";
import { TextInput, Button, HelperText } from "react-native-paper";
import LoginStyle from "../../styles/LoginStyle";
import { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import { useNavigation } from "@react-navigation/native";
import Apis, { endpoints } from "../../utils/Apis";

const Register = () => {
    const info = [
        { 
            label: "Tên", 
            field: "first_name", 
            icon: "text" 
        },
        { 
            label: "Họ và tên lót", 
            field: "last_name", 
            icon: "text" 
        },
        { 
            label: "Email", 
            field: "email", 
            icon: "email" 
        },
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
        },
        { 
            label: "Xác nhận mật khẩu", 
            field: "confirm", 
            icon: "eye", 
            secureTextEntry: true 
        }
    ];

    const [user, setUser] = useState({});
    const [errMsg, setErrMsg] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();

    const picker = async () => {
        const { granted } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (!granted) {
            Alert.alert("Không có quyền truy cập thư viện ảnh");
            return;
        }

        if (granted) {
            const res = await ImagePicker.launchImageLibraryAsync();
            if (!res.canceled)
                setUser({...user, "avatar": res.assets[0]});
        } else
            Alert.alert("Lỗi","Permission denied!");
    };

    const validate = () => {
        if (!user.first_name || !user.last_name || !user.username || !user.email) {
            setErrMsg("Vui lòng nhập đầy đủ thông tin cá nhân!");
            return false;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(user.email)) {
            setErrMsg("Email không hợp lệ!");
            return false;
        }
        if (!user.confirm || user.password !== user.confirm) {
            setErrMsg("Mật khẩu KHÔNG khớp!");
            return false;
        }
        setErrMsg(null);
        return true;
    };
    const register = async () => {
        if (validate()) {
            try {
                setLoading(true);
                let form = new FormData();
            
                for (let key in user) {
                    if (key !== 'confirm') {
                        if (key === 'avatar') {
                            form.append(key, {
                                uri: user.avatar.uri,
                                name: user.avatar.fileName,
                                type: "image/jpeg"
                            });
                        } else
                            form.append(key, user[key]);
                    }
                }
    
                let res = await Apis.post(endpoints['register'], form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
    
                if (res.status === 201) 
                    nav.navigate('Login');
                else
                    setErrMsg("Đã có lỗi xảy ra. Vui lòng thử lại sau!");
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
            <TouchableOpacity onPress={() => nav.goBack()}>
                <Text style={{ fontSize: 22 }}>✕</Text>
            </TouchableOpacity>
            <Text style={LoginStyle.title}>ĐĂNG KÝ NGƯỜI DÙNG</Text>
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
                    onChangeText={t => setUser({ ...user, [i.field]: t.trim() })}
                />
            ))}

            <TouchableOpacity style={{ marginTop: 10 }} onPress={picker}>
                <Text>Chọn ảnh đại diện...</Text>
            </TouchableOpacity>

            {user.avatar && ( <Image source={{ uri: user.avatar.uri }} style={LoginStyle.avatar}/>)}
            <Button mode="contained" loading={loading} disabled={loading} style={LoginStyle.loginBtn}  onPress={register}>
                <Text style={LoginStyle.loginText}>Đăng ký</Text>
            </Button>
        </View>
    );
};

export default Register;