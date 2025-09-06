#!/bin/bash

echo "🔧 Fixing Nginx configuration..."

# Remove existing symlink
echo "Removing existing symlink..."
sudo rm -f /etc/nginx/sites-enabled/smtp.truongvinhkhuong.io.vn

# Copy simple nginx config
echo "Copying simple nginx configuration..."
sudo cp nginx-simple.conf /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn

# Create symlink
echo "Creating symlink..."
sudo ln -s /etc/nginx/sites-available/smtp.truongvinhkhuong.io.vn /etc/nginx/sites-enabled/

# Remove default site
echo "Removing default site..."
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid!"
    
    # Reload nginx
    echo "Reloading nginx..."
    sudo systemctl reload nginx
    
    # Check nginx status
    echo "Checking nginx status..."
    sudo systemctl status nginx --no-pager
    
    echo ""
    echo "🎉 Nginx configuration fixed!"
    echo "Now you can run: sudo certbot --nginx -d smtp.truongvinhkhuong.io.vn"
else
    echo "❌ Nginx configuration test failed!"
    echo "Please check the configuration manually"
fi
