import { View, Text, TextInput, TouchableOpacity, Alert, Platform } from "react-native";
import { useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import DateTimePicker from "@react-native-community/datetimepicker";
import { authApis } from "../../utils/Apis";
import ReservationStyle from "../../styles/ReservationStyle";

const Reservation = () => {

    const [participants, setParticipants] = useState("");
    const [notes, setNotes] = useState("");
    const [date, setDate] = useState(new Date());
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showTimePicker, setShowTimePicker] = useState(false);
    const [loading, setLoading] = useState(false);

    const onChangeDate = (event, selectedDate) => {
        setShowDatePicker(false);
        if (event?.type === "dismissed") return;
        if (selectedDate) {
            const newDate = new Date(date);
            newDate.setFullYear(
                selectedDate.getFullYear(),
                selectedDate.getMonth(),
                selectedDate.getDate()
            );
            setDate(newDate);
        }
    };

    const onChangeTime = (event, selectedTime) => {
        setShowTimePicker(false);
        if (event?.type === "dismissed") return;
        if (selectedTime) {
            const newDate = new Date(date);
            newDate.setHours(
                selectedTime.getHours(),
                selectedTime.getMinutes()
            );
            setDate(newDate);
        }
    };
    const submitReservation = async () => {
        if (!participants || Number(participants) <= 0) {
            Alert.alert("Lỗi", "Vui lòng nhập số người hợp lệ");
            return;
        }
        if (date < new Date()) {
            Alert.alert("Lỗi", "Không thể đặt bàn trong quá khứ");
            return;
        }
        try {
            setLoading(true);
            const token = await AsyncStorage.getItem("access_token");
            const api = authApis(token);
            await api.post("/apis/reservations/", {
                date: date.toISOString(),
                participants: Number(participants),
                note: notes
            });

            Alert.alert("Thành công", "Đặt bàn thành công");
            
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={ReservationStyle.container}>
            <Text style={ReservationStyle.title}>Đặt bàn</Text>

            <Text style={ReservationStyle.label}>Ngày đặt bàn</Text>
            <TouchableOpacity
                style={ReservationStyle.input}
                onPress={() => setShowDatePicker(true)}>
                <Text>{date.toLocaleDateString("vi-VN")}</Text>
            </TouchableOpacity>

            <Text style={ReservationStyle.label}>Giờ đặt bàn</Text>
            <TouchableOpacity
                style={ReservationStyle.input}
                onPress={() => setShowTimePicker(true)}>
                <Text>
                    {date.toLocaleTimeString("vi-VN")}
                </Text>
            </TouchableOpacity>

            {showDatePicker && (
                <DateTimePicker value={date} mode="date" onChange={onChangeDate}/>
            )}

            {showTimePicker && (
                <DateTimePicker value={date} mode="time" onChange={onChangeTime}/>
            )}

            <Text style={ReservationStyle.label}>Số người</Text>
            <TextInput
                placeholder="Nhập số người"
                keyboardType="numeric"
                value={participants}
                onChangeText={setParticipants}
                style={ReservationStyle.input}
            />

            <Text style={ReservationStyle.label}>Ghi chú (tuỳ chọn)</Text>
            <TextInput
                placeholder="Ví dụ: ngồi gần cửa sổ, có trẻ em..."
                value={notes}
                onChangeText={setNotes}
                multiline
                style={[ReservationStyle.input, ReservationStyle.textArea]}
            />

            <TouchableOpacity
                onPress={submitReservation}
                disabled={loading}
                style={ReservationStyle.submitBtn}>
                <Text style={ReservationStyle.submitText}>
                    {loading ? "Đang gửi..." : "Xác nhận đặt bàn"}
                </Text>
            </TouchableOpacity>
        </View>
    );
};

export default Reservation;
