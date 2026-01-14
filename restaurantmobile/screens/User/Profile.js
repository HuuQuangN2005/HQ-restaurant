import { Alert, Text, TouchableOpacity, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import ProfileStyle from "../../styles/ProfileStyle";
import { useNavigation } from "@react-navigation/native";
import { useContext } from "react";
import { MyUserContext } from "../../utils/MyContext";
import AsyncStorage from "@react-native-async-storage/async-storage";

const Profile = () => {
    const navigation = useNavigation();
    const [user, dispatch] = useContext(MyUserContext);

    const MenuItem = ({ title, onPress }) => (
        <TouchableOpacity style={ProfileStyle.menuItem} onPress={onPress}>
            <Text style={ProfileStyle.menuText}>{title}</Text>
            <Ionicons name="chevron-forward-outline" size={20} color="#999" />
        </TouchableOpacity>
    );

    if (!user) {
        return (
            <View style={ProfileStyle.container}>
                <Text>Bạn chưa đăng nhập</Text>
            </View>
        );
    }

    const logout = async () => {
        await AsyncStorage.removeItem("access_token");
        dispatch({
            type: "logout",
        });
    };

    return (
        <View style={ProfileStyle.container}>
            <View style={ProfileStyle.userBox}>
                <View style={ProfileStyle.avatarWrapper}>
                    <Ionicons name="person-circle" size={90} color="#f5a623" />
                </View>

                <Text style={ProfileStyle.welcomeText}>
                    Chào {user.first_name}
                </Text>

                <Text style={ProfileStyle.userSubText}>
                    Chúc bạn có bữa ăn ngon miệng
                </Text>
            </View>

            <View style={ProfileStyle.menu}>
                <MenuItem title="Chức năng đầu bếp" 
                    onPress={() => {
                        if (user.role === "Cooker" && user.is_approved === true) {
                            navigation.navigate("ChefProfile");
                        }
                        else Alert.alert("Thông báo","Chức năng này chỉ dành cho đầu bếp đã được cấp phép.");
                    }}
                />
                
                <MenuItem title="Chức năng của quản lý" 
                    onPress={() => {
                        if (user.role === "Cooker" && user.is_approved === true) {
                            navigation.navigate("StaffManager");
                        }
                        else Alert.alert("Thông báo","Chức năng này chỉ dành cho quản trị viên và đầu bếp đã được cấp phép.");
                    }}
                />

                <MenuItem title="Đặt bàn" onPress={() => navigation.navigate("Reservation")}/>
                <MenuItem title="Thay đổi ngôn ngữ" onPress={()=>{
                    Alert.alert("Thông báo","Comming soon...");
                }}/>
                <MenuItem title="Hỗ trợ" onPress={()=>{
                    Alert.alert("Thông báo","Comming soon...");
                }}/>
                <MenuItem title="Chính sách và điều khoản" onPress={()=>{
                    Alert.alert("Thông báo","Comming soon...");
                }}/>
            </View>
            <TouchableOpacity style={ProfileStyle.logoutBtn} onPress={logout}>
                <Text style={ProfileStyle.logoutText}>Đăng xuất</Text>
            </TouchableOpacity>
        </View>
    );
};

export default Profile;
