package com.example.bletester;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattServer;
import android.bluetooth.BluetoothGattServerCallback;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.le.AdvertiseCallback;
import android.bluetooth.le.AdvertiseData;
import android.bluetooth.le.AdvertiseSettings;
import android.bluetooth.le.BluetoothLeAdvertiser;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.ParcelUuid;
import android.renderscript.ScriptGroup;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.SpannableStringBuilder;
import android.util.Log;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.util.UUID;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    // uuid
    private static final UUID UUID_SERVICE = UUID.fromString("00000000-0000-0000-0000-000000000000");
    private static final UUID UUID_CHARACTERISTIC1 = UUID.fromString("00000000-0000-0000-0000-000000000001");
    private static final UUID UUID_CHARACTERISTIC2 = UUID.fromString("00000000-0000-0000-0000-000000000002");


    // system object
    private InputMethodManager mInputMethodManager;


    // ble object
    private BluetoothManager mBluetoothManager = null;
    private BluetoothAdapter mBluetoothAdapter = null;
    private AdvertiseSettings mBluetoothAdvertiseSettings = null;
    private AdvertiseData mBluetoothAdvertiseData = null;
    private BluetoothLeAdvertiser mBluetoothAdvertiser = null;
    private AdvertiseCallback mBluetoothAdvertiseCallback = null;
    private BluetoothGattServer mBluetoothGattServer = null;
    private BluetoothGattServerCallback mBluetoothGattServerCallback = null;
    private BluetoothGattCharacteristic mBluetoothGattCharacteristic1 = null;
    private BluetoothGattCharacteristic mBluetoothGattCharacteristic2 = null;
    private BluetoothDevice mBluetoothDevice_Connecting = null;


    // layout object
    private LinearLayout mLinearLayout_Background;
    private TextView mTextView_Status;
    private TextView mTextView_Connect;
    private EditText mEditText_UUID1;
    private EditText mEditText_UUID2;
    private Button mButton_UUID1;
    private Button mButton_UUID2;
    private Button mButton_AdvertiseStart;
    private Button mButton_AdvertiseStop;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // get object
        mInputMethodManager = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        mLinearLayout_Background = (LinearLayout) findViewById(R.id.linearlayout_background);
        mTextView_Status = (TextView) findViewById(R.id.textview_status);
        mTextView_Connect = (TextView) findViewById(R.id.textview_connect);
        mEditText_UUID1 = (EditText) findViewById(R.id.edittext_uuid1);
        mEditText_UUID2 = (EditText) findViewById(R.id.edittext_uuid2);
        mButton_UUID1 = (Button) findViewById(R.id.button_uuid1);
        mButton_UUID2 = (Button) findViewById(R.id.button_uuid2);
        mButton_AdvertiseStart = (Button) findViewById(R.id.button_advertise_start);
        mButton_AdvertiseStop = (Button) findViewById(R.id.button_advertise_stop);

        // set listener
        mButton_UUID1.setOnClickListener(this);
        mButton_UUID2.setOnClickListener(this);
        mButton_AdvertiseStart.setOnClickListener(this);
        mButton_AdvertiseStop.setOnClickListener(this);

        // init active
        mButton_AdvertiseStart.setEnabled(true);
        mButton_AdvertiseStop.setEnabled(false);
        mButton_UUID1.setEnabled(false);
        mButton_UUID2.setEnabled(false);

        // init ble
        onCreate_Bluetooth();
    }

    private void onCreate_Bluetooth() {
        // check ble support
        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
            Toast.makeText(this, "don't support ble.", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        // get bluetooth adapter
        mBluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        mBluetoothAdapter = mBluetoothManager.getAdapter();
        if (null == mBluetoothAdapter) {
            Toast.makeText(this, "don't support bluetooth.", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        // init advertiser
        onCreate_Bluetooth_Advertiser();

        // init gatt server
        onCreate_Bluetooth_GattServer();
    }

    private void onCreate_Bluetooth_Advertiser() {
        // Bluetoothアドバタイザーの取得
        mBluetoothAdvertiser = mBluetoothAdapter.getBluetoothLeAdvertiser();
        if(null == mBluetoothAdvertiser) {
            Toast.makeText(this, "DON'T SUPPORT ADVERTISER.", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        // setAdvertiseMode アドバタイジングモードでコントロールする発信電力とレイテンシを設定できます
        // setConnectable	アドバタイジングの種類を接続か非接続か選択できます。
        // setTimeout	    アドバタイジングする時間を制限できます。0の場合は制限しません。
        // setConnectable	TX電力パワーレベルを設定できます
        AdvertiseSettings.Builder settingBuilder = new AdvertiseSettings.Builder();
        settingBuilder.setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_BALANCED);
        settingBuilder.setConnectable(true);
        settingBuilder.setTimeout(0);
        settingBuilder.setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_MEDIUM);
        mBluetoothAdvertiseSettings = settingBuilder.build();

        // addManufacturerData	manufacturer specific dataを追加できます。
        // addServiceData	    アドバタジングデータのためのServiceUUIDと送信データを追加します
        // addServiceUuid	    アドバタジングデータのためのServiceUUIDを追加します。
        AdvertiseData.Builder dataBuilder = new AdvertiseData.Builder();
        dataBuilder.addServiceUuid(new ParcelUuid(UUID_SERVICE));
        mBluetoothAdvertiseData = dataBuilder.build();

        // init callback
        onCreate_Bluetooth_Advertise_Callback();
    }

    private void onCreate_Bluetooth_Advertise_Callback() {
        mBluetoothAdvertiseCallback = new AdvertiseCallback() {
            @Override
            public void onStartSuccess(AdvertiseSettings settingsInEffect) {
                super.onStartSuccess(settingsInEffect);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Advertise success.", Toast.LENGTH_SHORT).show();
                    }
                });
            }
            @Override
            public void onStartFailure(int errorCode) {
                super.onStartFailure(errorCode);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Advertise failure.", Toast.LENGTH_SHORT).show();
                    }
                });
            }
        };
    }

    private void onCreate_Bluetooth_GattServer() {

        onCreate_Bluetooth_GattServer_Callback();
        mBluetoothGattServer = mBluetoothManager.openGattServer(getApplicationContext(), mBluetoothGattServerCallback);

        // create service
        BluetoothGattService service = new BluetoothGattService(
                UUID_SERVICE,
                BluetoothGattService.SERVICE_TYPE_PRIMARY);

        // create characteristic
        mBluetoothGattCharacteristic1 = new BluetoothGattCharacteristic(
                UUID_CHARACTERISTIC1,
                BluetoothGattCharacteristic.PROPERTY_NOTIFY | BluetoothGattCharacteristic.PROPERTY_READ | BluetoothGattCharacteristic.PROPERTY_WRITE,
                BluetoothGattCharacteristic.PERMISSION_READ | BluetoothGattCharacteristic.PERMISSION_WRITE);
        mBluetoothGattCharacteristic2 = new BluetoothGattCharacteristic(
                UUID_CHARACTERISTIC2,
                BluetoothGattCharacteristic.PROPERTY_NOTIFY | BluetoothGattCharacteristic.PROPERTY_READ | BluetoothGattCharacteristic.PROPERTY_WRITE,
                BluetoothGattCharacteristic.PERMISSION_READ | BluetoothGattCharacteristic.PERMISSION_WRITE);

        // set characteristic
        service.addCharacteristic(mBluetoothGattCharacteristic1);
        service.addCharacteristic(mBluetoothGattCharacteristic2);

        // set service
        mBluetoothGattServer.addService(service);
    }

    private void onCreate_Bluetooth_GattServer_Callback() {
        mBluetoothGattServerCallback = new BluetoothGattServerCallback() {
            @Override
            public void onConnectionStateChange(BluetoothDevice device, int status, int newState) {
                super.onConnectionStateChange(device, status, newState);
                System.out.println("debug log : " + newState);
                if(newState == BluetoothProfile.STATE_CONNECTED) {
                    mTextView_Connect.setText(device.getName());
                    mBluetoothDevice_Connecting = device;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            ((TextView)findViewById(R.id.textview_status)).setText("Connected.");
                            ((Button)findViewById(R.id.button_uuid1)).setEnabled(true);
                            ((Button)findViewById(R.id.button_uuid2)).setEnabled(true);
                        }
                    });
                }
                if(newState == BluetoothProfile.STATE_DISCONNECTED) {
                    mTextView_Connect.setText("");
                    mBluetoothDevice_Connecting = null;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            ((TextView)findViewById(R.id.textview_status)).setText("Disonnected.");
                            ((Button)findViewById(R.id.button_uuid1)).setEnabled(false);
                            ((Button)findViewById(R.id.button_uuid2)).setEnabled(false);
                        }
                    });
                }
            }

            @Override
            public void onCharacteristicReadRequest(BluetoothDevice device, int requestId, int offset, BluetoothGattCharacteristic characteristic) {
                super.onCharacteristicReadRequest(device, requestId, offset, characteristic);
            }

            @Override
            public void onCharacteristicWriteRequest(BluetoothDevice device, int requestId, BluetoothGattCharacteristic characteristic, boolean preparedWrite, boolean responseNeeded, int offset, byte[] value) {
                super.onCharacteristicWriteRequest(device, requestId, characteristic, preparedWrite, responseNeeded, offset, value);
            }

            @Override
            public void onExecuteWrite(BluetoothDevice device, int requestId, boolean execute) {
                super.onExecuteWrite(device, requestId, execute);
            }

            @Override
            public void onNotificationSent(BluetoothDevice device, int status) {
                super.onNotificationSent(device, status);
            }

            @Override
            public void onPhyUpdate(BluetoothDevice device, int txPhy, int rxPhy, int status) {
                super.onPhyUpdate(device, txPhy, rxPhy, status);
            }
        };
    }


    @Override
    public void onClick(View v) {
        if (mButton_UUID1.getId() == v.getId()) onClick_UUID(v);
        if (mButton_UUID2.getId() == v.getId()) onClick_UUID(v);
        if (mButton_AdvertiseStart.getId() == v.getId()) onClick_Advertise(true);
        if (mButton_AdvertiseStop.getId() == v.getId()) onClick_Advertise(false);
    }

    private void onClick_Advertise(boolean b) {
        if(b == true) {
            mBluetoothAdvertiser.startAdvertising(mBluetoothAdvertiseSettings, mBluetoothAdvertiseData, mBluetoothAdvertiseCallback);
            mTextView_Status.setText("Start advertise.");
            mButton_AdvertiseStart.setEnabled(false);
            mButton_AdvertiseStop.setEnabled(true);
        }
        if(b == false) {
            mBluetoothAdvertiser.stopAdvertising(mBluetoothAdvertiseCallback);
            mTextView_Status.setText("Stop advertise.");
            mButton_AdvertiseStart.setEnabled(true);
            mButton_AdvertiseStop.setEnabled(false);
        }
    }

    private void onClick_UUID(View v) {
        // check connecting device
        if (mBluetoothDevice_Connecting == null)
            return;

        // get EditText
        EditText targetEditText = null;
        BluetoothGattCharacteristic targetCharacteristic = null;
        if (mButton_UUID1.getId() == v.getId()) {
            targetEditText = mEditText_UUID1;
            targetCharacteristic = mBluetoothGattCharacteristic1;
        }
        if (mButton_UUID2.getId() == v.getId()) {
            targetEditText = mEditText_UUID2;
            targetCharacteristic = mBluetoothGattCharacteristic2;
        }

        // get text
        String text = ((SpannableStringBuilder) targetEditText.getText()).toString();

        // change characteristic and notify
        targetCharacteristic.setValue(text);
        mBluetoothGattServer.notifyCharacteristicChanged(
                mBluetoothDevice_Connecting, targetCharacteristic, false);
    }



    public void onTouchBackground(View view) {
        // Hide keyboard
        mInputMethodManager.hideSoftInputFromWindow(mLinearLayout_Background.getWindowToken(), InputMethodManager.HIDE_NOT_ALWAYS);

        // set focus
        mLinearLayout_Background.requestFocus();
    }
}