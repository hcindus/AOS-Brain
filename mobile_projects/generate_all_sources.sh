#!/bin/bash
# Master script to generate all source files for 11 Android projects

cd /root/.openclaw/workspace/mobile_projects

echo "========================================="
echo "GENERATING ANDROID PROJECT SOURCE FILES"
echo "========================================="

# Function to create basic Activity
create_activity() {
    local project=$1
    local package=$2
    local activity=$3
    
    mkdir -p "$project/app/src/main/java/$package"
    
    cat > "$project/app/src/main/java/$package/$activity.kt" << EOF
package $package

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class $activity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_${activity,,})
    }
}
EOF
}

# 1. Dusty Wallet - Additional Activities
create_activity "dusty-wallet" "com.agi.dusty.ui" "CreateWalletActivity"
create_activity "dusty-wallet" "com.agi.dusty.ui" "ImportWalletActivity"
create_activity "dusty-wallet" "com.agi.dusty.ui" "WalletActivity"
create_activity "dusty-wallet" "com.agi.dusty.ui" "TradingActivity"
create_activity "dusty-wallet" "com.agi.dusty.ui" "SettingsActivity"

# 2. UncleShield AV
create_activity "uncleshield-av" "com.agi.uncleshield.ui" "MainActivity"
create_activity "uncleshield-av" "com.agi.uncleshield.scanner" "ScannerActivity"
create_activity "uncleshield-av" "com.agi.uncleshield.protection" "ProtectionActivity"

mkdir -p uncleshield-av/app/src/main/java/com/agi/uncleshield
cat > uncleshield-av/app/src/main/java/com/agi/uncleshield/UncleShieldApplication.kt << 'EOF'
package com.agi.uncleshield

import android.app.Application

class UncleShieldApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 3. ReggieStarr POS
create_activity "reggiestarr-pos" "com.agi.reggiestarr.ui" "MainActivity"
create_activity "reggiestarr-pos" "com.agi.reggiestarr.pos" "CheckoutActivity"
create_activity "reggiestarr-pos" "com.agi.reggiestarr.inventory" "InventoryActivity"
create_activity "reggiestarr-pos" "com.agi.reggiestarr.reports" "ReportsActivity"

mkdir -p reggiestarr-pos/app/src/main/java/com/agi/reggiestarr
cat > reggiestarr-pos/app/src/main/java/com/agi/reggiestarr/POSApplication.kt << 'EOF'
package com.agi.reggiestarr

import android.app.Application

class POSApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 4. CREAM
create_activity "cream" "com.agi.cream.ui" "MainActivity"
create_activity "cream" "com.agi.cream.properties" "PropertyListActivity"
create_activity "cream" "com.agi.cream.clients" "ClientActivity"
create_activity "cream" "com.agi.cream.schedule" "ScheduleActivity"
create_activity "cream" "com.agi.cream.calculator" "CalculatorActivity"

mkdir -p cream/app/src/main/java/com/agi/cream
cat > cream/app/src/main/java/com/agi/cream/CREAMApplication.kt << 'EOF'
package com.agi.cream

import android.app.Application

class CREAMApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 5. Milk Man Games
create_activity "milkman-game" "com.agi.milkman.ui" "MainActivity"
create_activity "milkman-game" "com.agi.milkman.game2d" "Game2DActivity"
create_activity "milkman-game" "com.agi.milkman.game3d" "Game3DActivity"

# 6. Leche Games
create_activity "leche-game" "com.agi.leche.ui" "MainActivity"
create_activity "leche-game" "com.agi.leche.games2d" "Games2DActivity"
create_activity "leche-game" "com.agi.leche.games3d" "Games3DActivity"
create_activity "leche-game" "com.agi.leche.wrestling" "WrestlingGameActivity"

# 7. AM Hud Supplies
create_activity "amhud-supplies" "com.agi.amhud.ui" "MainActivity"
create_activity "amhud-supplies" "com.agi.amhud.catalog" "CatalogActivity"
create_activity "amhud-supplies" "com.agi.amhud.orders" "OrderActivity"
create_activity "amhud-supplies" "com.agi.amhud.account" "AccountActivity"

mkdir -p amhud-supplies/app/src/main/java/com/agi/amhud
cat > amhud-supplies/app/src/main/java/com/agi/amhud/AMHudApplication.kt << 'EOF'
package com.agi.amhud

import android.app.Application

class AMHudApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 8. TappyLewis
create_activity "tappylewis" "com.agi.tappylewis.ui" "MainActivity"
create_activity "tappylewis" "com.agi.tappylewis.booking" "BookingActivity"
create_activity "tappylewis" "com.agi.tappylewis.services" "ServicesActivity"
create_activity "tappylewis" "com.agi.tappylewis.profile" "ProfileActivity"

mkdir -p tappylewis/app/src/main/java/com/agi/tappylewis
cat > tappylewis/app/src/main/java/com/agi/tappylewis/TappyLewisApplication.kt << 'EOF'
package com.agi.tappylewis

import android.app.Application

class TappyLewisApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 9. Secretarial Pool
create_activity "secretarial-pool" "com.agi.secretarial.ui" "MainActivity"
create_activity "secretarial-pool" "com.agi.secretarial.admin" "AdminActivity"
create_activity "secretarial-pool" "com.agi.secretarial.documents" "DocumentsActivity"
create_activity "secretarial-pool" "com.agi.secretarial.tasks" "TasksActivity"

mkdir -p secretarial-pool/app/src/main/java/com/agi/secretarial
cat > secretarial-pool/app/src/main/java/com/agi/secretarial/SecretarialApplication.kt << 'EOF'
package com.agi.secretarial

import android.app.Application

class SecretarialApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 10. PS Depot Supplies
create_activity "psdepot-supplies" "com.agi.psdepot.ui" "MainActivity"
create_activity "psdepot-supplies" "com.agi.psdepot.catalog" "CatalogActivity"
create_activity "psdepot-supplies" "com.agi.psdepot.orders" "OrderActivity"
create_activity "psdepot-supplies" "com.agi.psdepot.supplies" "SuppliesActivity"

mkdir -p psdepot-supplies/app/src/main/java/com/agi/psdepot
cat > psdepot-supplies/app/src/main/java/com/agi/psdepot/PSDepotApplication.kt << 'EOF'
package com.agi.psdepot

import android.app.Application

class PSDepotApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

# 11. DepotChaos CRM
create_activity "depotcrm" "com.agi.depotcrm.ui" "MainActivity"
create_activity "depotcrm" "com.agi.depotcrm.leads" "LeadsActivity"
create_activity "depotcrm" "com.agi.depotcrm.contacts" "ContactsActivity"
create_activity "depotcrm" "com.agi.depotcrm.deals" "DealsActivity"
create_activity "depotcrm" "com.agi.depotcrm.analytics" "AnalyticsActivity"

mkdir -p depotcrm/app/src/main/java/com/agi/depotcrm
cat > depotcrm/app/src/main/java/com/agi/depotcrm/CRMApplication.kt << 'EOF'
package com.agi.depotcrm

import android.app.Application

class CRMApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
EOF

echo "========================================="
echo "Activity files created for all projects"
echo "========================================="
