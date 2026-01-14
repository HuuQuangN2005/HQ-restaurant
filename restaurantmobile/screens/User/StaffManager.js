import { Alert, Text, TouchableOpacity, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import ChefProfileStyle from "../../styles/ChefProfileStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";
import { useContext, useEffect } from "react";
import { MyUserContext } from "../../utils/MyContext";

const StaffManager = () => {
    const nav = useNavigation();
    const [user] = useContext(MyUserContext);

    useEffect(() => {
        if (!user) {
            nav.navigate("Main");
            return;
        }
        const isChef =
            (user.role === "Cooker" || user.is_staff === 1) &&
            (user.is_approved === true || user.is_approved === 1);
        if (!isChef) {
            Alert.alert(
                "Thông báo",
                "Bạn không có quyền truy cập chức năng này."
            );
            nav.goBack();
        }
    }, [user]);

    const ChefItem = ({ title, onPress }) => (
        <TouchableOpacity
            style={ChefProfileStyle.menuItem}
            onPress={onPress}
        >
            <Text style={ChefProfileStyle.menuText}>{title}</Text>
            <Ionicons
                name="chevron-forward-outline"
                size={20}
                style={ChefProfileStyle.menuIcon}
            />
        </TouchableOpacity>
    );

    return (
        <View style={ChefProfileStyle.container}>
            <TouchableOpacity onPress={() => nav.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <View style={ChefProfileStyle.header}>
                <Text style={ChefProfileStyle.title}>
                    Chức năng cho Nhân viên
                </Text>
                <Text style={ChefProfileStyle.subtitle}>
                    Quản lý hoạt động và hiệu quả kinh doanh
                </Text>
            </View>

            <View style={ChefProfileStyle.menu}>
                <ChefItem
                    title="Quản lý đặt chỗ"
                    onPress={() => nav.navigate("ReservationManager")}
                />
                <ChefItem
                    title="Quản lý đặt hàng"
                    onPress={() => nav.navigate("StaffOrders")}
                />
            </View>
        </View>
    );
};

export default StaffManager;
