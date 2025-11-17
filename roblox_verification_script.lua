-- Script Lua pour Roblox - Vérification Discord
-- Placez ce script dans ServerScriptService
--
-- INSTRUCTIONS:
-- 1. Assurez-vous que votre bot Discord est actif et que le serveur web tourne
-- 2. Trouvez l'IP de votre serveur (ipconfig sur Windows, ifconfig sur Linux)
-- 3. Remplacez "VOTRE_IP" par votre IP à la ligne 189 ci-dessous
-- 4. Le bot détectera automatiquement les codes envoyés via le serveur web

local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local StarterGui = game:GetService("StarterGui")

-- Fonction pour générer un code unique
local function generateCode()
    local chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    local code = ""
    for i = 1, 8 do
        local rand = math.random(1, #chars)
        code = code .. string.sub(chars, rand, rand)
    end
    return code
end

-- Créer une interface utilisateur en plein écran
local function createVerificationGUI(player, code)
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "DiscordVerification"
    screenGui.ResetOnSpawn = false
    screenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    screenGui.IgnoreGuiInset = true
    screenGui.Parent = player.PlayerGui

    -- Empêcher le joueur de bouger
    local character = player.Character or player.CharacterAdded:Wait()
    if character then
        local humanoid = character:WaitForChild("Humanoid", 10)
        if humanoid then
            humanoid.WalkSpeed = 0
            humanoid.JumpPower = 0
        end
    end
    
    -- Fond sombre plein écran
    local background = Instance.new("Frame")
    background.Size = UDim2.new(1, 0, 1, 0)
    background.Position = UDim2.new(0, 0, 0, 0)
    background.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    background.BackgroundTransparency = 0.3
    background.BorderSizePixel = 0
    background.Parent = screenGui

    -- Container principal au centre
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(0, 700, 0, 550)
    frame.Position = UDim2.new(0.5, -350, 0.5, -275)
    frame.BackgroundColor3 = Color3.fromRGB(54, 57, 63)
    frame.BorderSizePixel = 0
    frame.Parent = screenGui
    
    -- Coins arrondis
    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 12)
    corner.Parent = frame

    -- Ombre/Contour du container
    local stroke = Instance.new("UIStroke")
    stroke.Thickness = 2
    stroke.Color = Color3.fromRGB(88, 101, 242)
    stroke.Parent = frame

    -- Titre
    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, -40, 0, 80)
    title.Position = UDim2.new(0, 20, 0, 20)
    title.BackgroundTransparency = 1
    title.Text = "🔐 VÉRIFICATION DISCORD"
    title.TextColor3 = Color3.fromRGB(255, 255, 255)
    title.TextSize = 32
    title.Font = Enum.Font.GothamBold
    title.TextXAlignment = Enum.TextXAlignment.Left
    title.TextYAlignment = Enum.TextYAlignment.Center
    title.Parent = frame

    -- Sous-titre
    local subtitle = Instance.new("TextLabel")
    subtitle.Size = UDim2.new(1, -40, 0, 50)
    subtitle.Position = UDim2.new(0, 20, 0, 90)
    subtitle.BackgroundTransparency = 1
    subtitle.Text = "Vous devez vérifier votre compte Discord pour continuer"
    subtitle.TextColor3 = Color3.fromRGB(150, 150, 150)
    subtitle.TextSize = 18
    subtitle.Font = Enum.Font.Gotham
    subtitle.TextXAlignment = Enum.TextXAlignment.Left
    subtitle.TextYAlignment = Enum.TextYAlignment.Center
    subtitle.Parent = frame

    -- Séparateur
    local divider = Instance.new("Frame")
    divider.Size = UDim2.new(1, -40, 0, 2)
    divider.Position = UDim2.new(0, 20, 0, 150)
    divider.BackgroundColor3 = Color3.fromRGB(88, 101, 242)
    divider.BorderSizePixel = 0
    divider.Parent = frame

    local instruction = Instance.new("TextLabel")
    instruction.Size = UDim2.new(1, -40, 0, 80)
    instruction.Position = UDim2.new(0, 20, 0, 170)
    instruction.BackgroundTransparency = 1
    instruction.Text = "1️⃣ Sélectionnez et copiez le code ci-dessous\n2️⃣ Utilisez /verify sur Discord avec votre nom Roblox et ce code"
    instruction.TextColor3 = Color3.fromRGB(200, 200, 200)
    instruction.TextSize = 16
    instruction.TextWrapped = true
    instruction.Font = Enum.Font.Gotham
    instruction.TextXAlignment = Enum.TextXAlignment.Left
    instruction.TextYAlignment = Enum.TextYAlignment.Top
    instruction.Parent = frame

    -- Code à copier
    local codeLabel = Instance.new("TextLabel")
    codeLabel.Size = UDim2.new(1, -40, 0, 40)
    codeLabel.Position = UDim2.new(0, 20, 0, 260)
    codeLabel.BackgroundTransparency = 1
    codeLabel.Text = "Votre code unique :"
    codeLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    codeLabel.TextSize = 14
    codeLabel.Font = Enum.Font.GothamBold
    codeLabel.TextXAlignment = Enum.TextXAlignment.Left
    codeLabel.Parent = frame

    -- Zone de texte sélectionnable pour le code
    local codeDisplay = Instance.new("TextBox")
    codeDisplay.Size = UDim2.new(1, -40, 0, 100)
    codeDisplay.Position = UDim2.new(0, 20, 0, 300)
    codeDisplay.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    codeDisplay.BorderSizePixel = 2
    codeDisplay.BorderColor3 = Color3.fromRGB(88, 101, 242)
    codeDisplay.Text = code
    codeDisplay.TextColor3 = Color3.fromRGB(88, 101, 242)
    codeDisplay.TextSize = 56
    codeDisplay.Font = Enum.Font.GothamBold
    codeDisplay.TextXAlignment = Enum.TextXAlignment.Center
    codeDisplay.TextYAlignment = Enum.TextYAlignment.Center
    codeDisplay.PlaceholderText = ""
    codeDisplay.ClearTextOnFocus = false
    codeDisplay.TextEditable = false  -- Empêcher l'édition mais permettre la sélection
    codeDisplay.Parent = frame
    
    -- Coins arrondis pour le code
    local codeCorner = Instance.new("UICorner")
    codeCorner.CornerRadius = UDim.new(0, 8)
    codeCorner.Parent = codeDisplay
    
    -- Focus automatique pour sélectionner tout le texte
    codeDisplay:CaptureFocus()
    task.wait(0.1)
    codeDisplay:ReleaseFocus()

    local statusLabel = Instance.new("TextLabel")
    statusLabel.Size = UDim2.new(1, -40, 0, 60)
    statusLabel.Position = UDim2.new(0, 20, 0, 410)
    statusLabel.BackgroundTransparency = 1
    statusLabel.Text = "⏳ En attente de vérification Discord..."
    statusLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
    statusLabel.TextSize = 18
    statusLabel.Font = Enum.Font.Gotham
    statusLabel.TextWrapped = true
    statusLabel.TextXAlignment = Enum.TextXAlignment.Left
    statusLabel.TextYAlignment = Enum.TextYAlignment.Center
    statusLabel.Parent = frame

    local warningLabel = Instance.new("TextLabel")
    warningLabel.Size = UDim2.new(1, -40, 0, 50)
    warningLabel.Position = UDim2.new(0, 20, 0, 470)
    warningLabel.BackgroundTransparency = 1
    warningLabel.Text = "⚠️ Cette fenêtre restera affichée jusqu'à votre vérification sur Discord"
    warningLabel.TextColor3 = Color3.fromRGB(255, 193, 7)
    warningLabel.TextSize = 14
    warningLabel.Font = Enum.Font.Gotham
    warningLabel.TextWrapped = true
    warningLabel.TextXAlignment = Enum.TextXAlignment.Left
    warningLabel.TextYAlignment = Enum.TextYAlignment.Center
    warningLabel.Parent = frame

    return screenGui
end

-- ⚠️ CONFIGURATION REQUISE: Remplacez cette URL par l'IP de votre serveur Discord
local WEB_SERVER_URL = "http://10.252.160.1:5000/verify"  -- Serveur web Flask

-- Quand un joueur rejoint
Players.PlayerAdded:Connect(function(player)
    task.wait(2)  -- Attendre que le joueur charge complètement
    local code = generateCode()
    print("[VERIFICATION] Code généré pour " .. player.Name .. ": " .. code)
    
    -- Envoyer le code via le serveur web
    if WEB_SERVER_URL ~= "" and not string.find(WEB_SERVER_URL, "VOTRE_IP") then
        local payload = {
            code = code,
            username = player.Name
        }
        
        local success, response = pcall(function()
            return HttpService:PostAsync(
                WEB_SERVER_URL,
                HttpService:JSONEncode(payload)
            )
        end)
        
        if success then
            print("[VERIFICATION] Code envoyé au serveur web pour " .. player.Name)
        else
            warn("[VERIFICATION] Erreur lors de l'envoi au serveur web: " .. tostring(response))
        end
    end
    
    local gui = createVerificationGUI(player, code)
    
    -- Expulser après 5 minutes si non vérifié
    task.delay(300, function()
        if gui.Parent then
            player:Kick("Temps de vérification écoulé. Rejoignez et vérifiez-vous dans les 5 minutes.")
        end
    end)
end)

-- Configuration CORS pour Roblox
HttpService.HttpEnabled = true

print("✅ Script de vérification Discord chargé")
